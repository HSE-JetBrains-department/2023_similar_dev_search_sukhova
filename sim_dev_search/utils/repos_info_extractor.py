from typing import List, Dict

from pydriller import Repository, ModifiedFile
from tqdm import tqdm


class ReposInfoExtractor:
    def __init__(self, repos_list: List[str]):
        self.repos_list = repos_list
        self.programmers_info = dict()

    def _extract_repo_info(self, path_to_repo: str) -> None:
        commits_count = 0

        for commit in Repository(path_to_repo).traverse_commits():
            commits_count += 1
        for commit in tqdm(Repository(path_to_repo).traverse_commits(),
                           total=commits_count, desc=f'Extracting from {path_to_repo}'):
            author_id = commit.author.email

            if author_id not in self.programmers_info:
                self.programmers_info[author_id] = {}
            commits_field_name = commit.author.name + "_commits"
            self.programmers_info[author_id][commits_field_name] = {}

            for file in commit.modified_files:
                self._add_file_info(author_id, commits_field_name, file)

    def _add_file_info(self, author_id: str, commits_field_name: str, file: ModifiedFile) -> None:
        if file.filename not in self.programmers_info[author_id][commits_field_name]:
            self.programmers_info[author_id][commits_field_name][file.filename] = {"added": 0, "deleted": 0}
        self.programmers_info[author_id][commits_field_name][file.filename]["added"] += file.added_lines
        self.programmers_info[author_id][commits_field_name][file.filename]["deleted"] += file.deleted_lines

    def get_programmers_commits_info(self) -> Dict[str, dict]:
        if len(self.programmers_info) != 0:
            return self.programmers_info
        for repo in self.repos_list:
            self._extract_repo_info(repo)

        return self.programmers_info
