from collections import Counter
from time import sleep
from typing import Any, Dict, List, Optional, Set, Union
from urllib.parse import urlparse

import requests


class StargazersTopExtractor:
    """
    Class that extracts information about repositories stargazers.
    """

    def __init__(
            self,
            repos_list: List[str],
            api_token: Optional[str] = None,
            repositories_top_size: int = 100,
            max_pages_count: int = 10**10
    ):
        """
        GitHub's repositories stargazers top repos extractor initialization.
        :param repos_list: List of paths to GitHub repositories.
        :param api_token: API access token.
        :param repositories_top_size: Size of repositories top list.
        :param max_pages_count: Maximum pages number to process.
        """
        self._repos_list = repos_list
        self._repositories_top_size = repositories_top_size
        self._max_pages_count = max_pages_count
        self._repositories_top = {}
        self._request_headers = {}

        if api_token:
            self._request_headers = {"Authorization": f"token {api_token}"}

    @staticmethod
    def _get_json_response(url: str, headers: Dict[str, str]) -> Union[Dict[str, str], List[Dict[str, Any]]]:
        """
        Get json response from URL.
        :param url: URL.
        :return: Json response.
        """
        response: Optional[Union[Dict[str, str], List[Dict[str, Any]]]] = None

        while response is None:
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=10,
                ).json()
            except requests.exceptions.Timeout:
                sleep_time = 5
                print(f"Connection refused by the server, waiting for {sleep_time} seconds...")
                sleep(sleep_time)
        return response

    def _get_stargazers(self, repo_url: str) -> Set[str]:
        """
        Get given repository stargazers.
        :param repo_url: URL to GitHub repository.
        :return: Set of repository stargazers.
        """
        stargazers = set()
        parsed_repo_url = urlparse(repo_url)
        url_template = parsed_repo_url._replace(netloc="api.github.com", path="/repos" + parsed_repo_url.path).geturl()
        url_template += "/stargazers?page={}&per_page=100"

        for page in range(1, self._max_pages_count + 1):
            response = self._get_json_response(
                url_template.format(page),
                headers=self._request_headers,
            )
            if (len(response) == 0) or isinstance(response, dict):
                break
            stargazers.update(map(lambda user: user["login"], response))
        return stargazers

    def _extract_starred_repos_info(self, stargazers: Set[str], *, early_stop: int = 0) -> Counter:
        """
        Extract starred repositories info from stargazers.
        :param stargazers: Set of repositories stargazers.
        :return: Counter of repositories stars from stargazers.
        """
        url_template = "https://api.github.com/users/{}/starred?page={}&per_page=100"
        starred_repos = Counter()
        repo_url_feature = "html_url"

        for stargazer_idx, stargazer in enumerate(stargazers):
            if early_stop and stargazer_idx >= early_stop:
                break
            for page in range(1, self._max_pages_count + 1):
                response = self._get_json_response(
                    url_template.format(stargazer, page),
                    self._request_headers,
                )
                if (len(response) == 0) or isinstance(response, dict):
                    break
                for repo in response:
                    starred_repos[repo[repo_url_feature]] += 1
        return starred_repos

    @property
    def repositories_top(self) -> Dict[str, int]:
        """
        Top GitHub repos in popularity among stargazers.
        :return: Top of repositories.
        """
        if self._repositories_top and len(self._repositories_top) <= self._repositories_top_size:
            return self._repositories_top
        stargazers = set()

        for repo in self._repos_list:
            stargazers |= self._get_stargazers(repo)
        starred_repos = self._extract_starred_repos_info(stargazers)
        self._repositories_top = dict(starred_repos.most_common(self._repositories_top_size))

        return self._repositories_top
