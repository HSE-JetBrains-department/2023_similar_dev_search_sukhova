import json
import unittest

from sim_dev_search.utils.repos_info_extractor import ReposInfoExtractor


class RepoExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = ReposInfoExtractor(['https://github.com/HSE-JetBrains-department'
                                             '/2022_similar_dev_search_kononov'])

    def test_repos_info_extractor(self):
        programmers_info = self.extractor.get_programmers_commits_info()

        with open('tests/repo_extractor_test_sample.json', 'r') as fp:
            programmers_info_sample = json.load(fp)
        self.assertEqual(programmers_info, programmers_info_sample)
