from collections import defaultdict
from typing import List, Dict

from pydriller import Repository, ModifiedFile
from tqdm import tqdm


class ReposInfoExtractor:
    def __init__(self, repos_list: List[str]):
        """
        GitHub's repositories info extractor initialization.
        :param repos_list: List of paths to GitHub repositories.
        """
        self.repos_list = repos_list
        self._programmers_info = defaultdict(dict)

    def _extract_repo_info(self, path_to_repo: str) -> None:
        """
        Extract info about programmers and their commits.
        :param path_to_repo: Path to GitHub repository.
        """
        commits_count = 0

        for _ in Repository(path_to_repo).traverse_commits():
            commits_count += 1
        for commit in tqdm(Repository(path_to_repo).traverse_commits(),
                           total=commits_count, desc=f"Extracting from {path_to_repo}"):
            author_id = commit.author.email
            commits_field_name = commit.author.name + "_commits"

            if commits_field_name not in self._programmers_info[author_id]:
                self._programmers_info[author_id][commits_field_name] = {}

            for file in commit.modified_files:
                self._add_file_info(author_id, commits_field_name, file)

    def _add_file_info(self, author_id: str, commits_field_name: str, file: ModifiedFile) -> None:
        """
        Add information about modified file to programmer information.
        :param author_id: Unique name of GitHub programmer.
        :param commits_field_name: Name of commit author.
        :param file: File from GitHub repository.
        """
        if file.filename not in self._programmers_info[author_id][commits_field_name]:
            self._programmers_info[author_id][commits_field_name][file.filename] = {"added": 0, "deleted": 0}
        self._programmers_info[author_id][commits_field_name][file.filename]["added"] += file.added_lines
        self._programmers_info[author_id][commits_field_name][file.filename]["deleted"] += file.deleted_lines

    @property
    def programmers_info(self) -> Dict[str, dict]:
        """
        Information about programmers and their commits from given repositories.
        :return: dictionary of programmers and their commits.
        """
        if len(self._programmers_info) != 0:
            return self._programmers_info
        for repo in self.repos_list:
            self._extract_repo_info(repo)
        return self._programmers_info
