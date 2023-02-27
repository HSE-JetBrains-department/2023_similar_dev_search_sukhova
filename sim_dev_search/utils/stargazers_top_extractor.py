from collections import defaultdict
from pathlib import Path
from typing import List, Dict

import requests


class StargazersTopExtractor:
    MAX_PAGES_COUNT = 10 ** 10
    REPOSITORIES_TOP_SIZE = 100

    def __init__(self, repos_list: List[str]):
        """
        GitHub's repositories stargazers top 100 repos extractor initialization.
        :param repos_list: List of paths to GitHub repositories.
        """
        self.repos_list = repos_list
        self._stargazers = set()
        self._starred_repos = defaultdict(int)
        self._repositories_top = list()

    def _get_stargazers(self, path_to_repo: str) -> None:
        """
        Get given repository stargazers.
        :param path_to_repo: Path to GitHub repository.
        """
        path_to_repo = Path(path_to_repo)
        url = f"https://api.github.com/repos/{path_to_repo.parts[-2]}/{path_to_repo.parts[-1]}"
        url += "/stargazers?page={}&per_page=100"

        for pages_count in range(1, self.MAX_PAGES_COUNT + 1):
            response = requests.get(url.format(pages_count)).json()

            if (len(response) == 0) or isinstance(response, dict):
                break
            self._stargazers.update(list(map(lambda user: user["login"], response)))

    def _extract_starred_repos_info(self) -> None:
        """
        Extract starred repositories info from stargazers.
        """
        url = "https://api.github.com/users/{}/starred?page={}&per_page=100"
        repo_url_feature = "html_url"

        for stargazer in self._stargazers:
            for pages_count in range(1, self.MAX_PAGES_COUNT + 1):
                response = requests.get(url.format(stargazer, pages_count)).json()

                if (len(response) == 0) or isinstance(response, dict):
                    break

                for repo in response:
                    self._starred_repos[repo[repo_url_feature]] += 1

    @property
    def repositories_top(self) -> List[str]:
        """
        Top 100 GitHub repos in popularity among stargazers.
        :return: list of repositories.
        """
        if (len(self._repositories_top) != 0) and \
           (len(self._repositories_top) <= self.REPOSITORIES_TOP_SIZE):
            return self._repositories_top
        for repo in self.repos_list:
            self._get_stargazers(repo)
        self._extract_starred_repos_info()

        self._repositories_top = list(map(
            lambda r: r[0], sorted(self._starred_repos.items(), key=lambda it: it[1], reverse=True)
        ))[:self.REPOSITORIES_TOP_SIZE]

        return self._repositories_top
