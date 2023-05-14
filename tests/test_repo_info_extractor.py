import pickle
import unittest
from pathlib import Path
from typing import List
from unittest import mock

from pydriller import ModifiedFile, Repository
from pydriller.domain.commit import Commit

from sim_dev_search.utils.repos_info_extractor import ReposInfoExtractor


@mock.patch.object(Repository, "traverse_commits")
@mock.patch.object(Commit, "modified_files", new_callable=mock.PropertyMock)
@mock.patch.object(Repository, "__new__")
class RepoExtractorTestCase(unittest.TestCase):
    COMMITS_NUMBER = 4
    DEVELOPERS_NUMBER = 2
    DEVELOPERS_ADDED_LINES = 15
    DEVELOPERS_DELETED_LINES = 5
    FILES_MODIFIED_NUMBER = 3

    def setUp(self):
        path_to_data_folder = Path(__file__).parent / "data"
        path_to_repo = path_to_data_folder / "repository_test_sample"
        path_template_to_commit = str(path_to_data_folder / "commits_{}_test_sample")
        path_template_to_files = str(path_to_data_folder / "modified_files_{}_test_sample")

        with open(path_to_repo, "rb") as f_in:
            self.repository: Repository = pickle.load(f_in)
        self.commits: List[Commit] = []
        self.modified_files: List[List[ModifiedFile]] = []

        for commit_idx in range(self.COMMITS_NUMBER):
            with open(path_to_data_folder / path_template_to_commit.format(commit_idx), "rb") as f_in:
                self.commits.append(pickle.load(f_in))
            with open(path_to_data_folder / path_template_to_files.format(commit_idx), "rb") as f_in:
                self.modified_files.append(pickle.load(f_in))

    def test_programmers_info(self, repo_mock, files_mock, commits_mock):
        repo_mock.return_value = self.repository
        commits_mock.return_value = self.commits
        files_mock.side_effect = self.modified_files

        test_repo_name = "test-repo"
        extractor = ReposInfoExtractor([test_repo_name])
        programmers_info = extractor.programmers_info

        self.assertEqual(len(programmers_info), self.DEVELOPERS_NUMBER)
        added_lines_cnt = sum(
            dev_info[test_repo_name]["changed_files"][filename]["added"]
            for dev_info in programmers_info.values() for filename in dev_info[test_repo_name]["changed_files"].keys()
        )
        self.assertEqual(added_lines_cnt, self.DEVELOPERS_ADDED_LINES)
        added_lines_cnt = sum(
            dev_info[test_repo_name]["changed_files"][filename]["deleted"]
            for dev_info in programmers_info.values() for filename in dev_info[test_repo_name]["changed_files"].keys()
        )
        self.assertEqual(added_lines_cnt, self.DEVELOPERS_DELETED_LINES)
        modified_files_cnt = len(
            set(
                filename for dev_info in programmers_info.values()
                for filename in dev_info[test_repo_name]["changed_files"].keys()
            )
        )
        self.assertEqual(modified_files_cnt, self.FILES_MODIFIED_NUMBER)
