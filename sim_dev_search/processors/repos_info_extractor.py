from collections import defaultdict, Counter
from typing import Dict, List

from pydriller import ModifiedFile, Repository
from tqdm import tqdm

from sim_dev_search.processors.tree_sitter.tree_sitter_extractor import TreeSitterExtractor
from ..utils.language_utils import extract_language


class ReposInfoExtractor:
    """
    Class that extracts information about repos programmers from commits.
    """

    LANGUAGE_FIELD = "languages"
    VARIABLES_FIELD = "variables"
    FILES_FIELD = "changed_files"

    def __init__(self, repos_list: List[str]):
        """
        GitHub's repositories info extractor initialization.
        :param repos_list: List of paths to GitHub repositories.
        """
        self.repos_list = repos_list
        self._programmers_info = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self._ts_extractor = TreeSitterExtractor()

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
                self._add_file_info(author_id, file, path_to_repo)

    def _add_file_info(self, author_id: str, file: ModifiedFile, repo_name: str) -> None:
        """
        Add information about modified file to developer information.
        :param author_id: Unique name of GitHub developer.
        :param file: File from GitHub repository.
        :param repo_name: Name of repository.
        """
        if file.filename not in self._programmers_info[author_id][repo_name][self.FILES_FIELD]:
            self._programmers_info[author_id][repo_name][self.FILES_FIELD][file.filename] = defaultdict(int)
        self._programmers_info[author_id][repo_name][self.FILES_FIELD][file.filename]["added"] += file.added_lines
        self._programmers_info[author_id][repo_name][self.FILES_FIELD][file.filename]["deleted"] += file.deleted_lines
        if file.content:
            file_language = extract_language(file.filename, file_content=file.content)
            self._programmers_info[author_id][repo_name][
                self.VARIABLES_FIELD
            ] = self._ts_extractor.extract_with_tree_sitter(language=file_language, source_code=file.content)
            self._programmers_info[author_id][repo_name].setdefault(self.LANGUAGE_FIELD, Counter())[file_language] += 1

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
