from collections import defaultdict, Counter
from typing import Dict, List

from pydriller import ModifiedFile, Repository
from tqdm import tqdm

from .language_utils import extract_language


class ReposInfoExtractor:
    """
    Class that extracts information about repos programmers from commits.
    """

    LANGUAGE_FIELD = "languages"
    FILES_FIELD = "changed_files"

    def __init__(self, repos_list: List[str]):
        """
        GitHub's repositories info extractor initialization.
        :param repos_list: List of paths to GitHub repositories.
        """
        self.repos_list = repos_list
        self._programmers_info = defaultdict(lambda: defaultdict(dict))

    def _extract_repo_info(self, path_to_repo: str) -> None:
        """
        Extract info about developers and their commits.
        :param path_to_repo: Path to GitHub repository.
        """
        commits_count = 0

        for _ in Repository(path_to_repo).traverse_commits():
            commits_count += 1
        for commit in tqdm(
            Repository(path_to_repo).traverse_commits(), total=commits_count, desc=f"Extracting from {path_to_repo}"
        ):
            author_id = commit.author.email

            for file in commit.modified_files:
                self._add_file_info(author_id, file)

    def _add_file_info(self, author_id: str, file: ModifiedFile) -> None:
        """
        Add information about modified file to developer information.
        :param author_id: Unique name of GitHub developer.
        :param file: File from GitHub repository.
        """
        if file.filename not in self._programmers_info[author_id][self.FILES_FIELD]:
            self._programmers_info[author_id][self.FILES_FIELD][file.filename] = defaultdict(int)
        self._programmers_info[author_id][self.FILES_FIELD][file.filename]["added"] += file.added_lines
        self._programmers_info[author_id][self.FILES_FIELD][file.filename]["deleted"] += file.deleted_lines
        if file.content:
            file_language = extract_language(file.filename, file_content=file.content)
            self._programmers_info[author_id].setdefault(self.LANGUAGE_FIELD, Counter())[file_language] += 1

    @property
    def programmers_info(self) -> Dict[str, dict]:
        """
        Information about developers and their commits from given repositories.
        :return: Dictionary of developers and their commits.
        """
        if len(self._programmers_info) != 0:
            return self._programmers_info
        for repo in self.repos_list:
            self._extract_repo_info(repo)
        return self._programmers_info
