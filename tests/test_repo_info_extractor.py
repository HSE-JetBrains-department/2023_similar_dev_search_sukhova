import json
import unittest
from pprint import pprint

from sim_dev_search.utils.repos_info_extractor import ReposInfoExtractor


class RepoExtractorTestCase(unittest.TestCase):
    def setUp(self):
        path_to_repo = "https://github.com/HSE-JetBrains-department/2022_similar_dev_search_kononov"
        self.extractor = ReposInfoExtractor([path_to_repo])

    def test_repos_info_extractor(self):
        programmers_info = self.extractor.programmers_info

        with open("tests/repo_extractor_test_sample.json", "r") as fp:
            programmers_info_sample = json.load(fp)
        self.assertEqual(dict(programmers_info), programmers_info_sample)
