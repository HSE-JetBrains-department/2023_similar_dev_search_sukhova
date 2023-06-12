import json
from collections import Counter
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import git
from tqdm import tqdm
from tree_sitter import Language, Parser


class TreeSitterExtractor:
    """
    Class that parses source code and extracts identifiers information.
    """

    BUILD_DIR = Path(__file__).resolve().parent / "build"
    BUILD_LANGUAGES_PATH = BUILD_DIR / "my-languages.so"
    CONFIG_PATH = Path(__file__).resolve().parent / "language_grammar_config.json"

    IDENTIFIERS_QUERY = "(identifier) @variable"

    def __init__(self):
        with open(self.CONFIG_PATH, "r", encoding="utf-8") as config_file:
            self.language_grammar_repos = json.load(config_file)
        self.clone_grammar_repos()
        self.build_library()

    def clone_grammar_repos(self) -> None:
        """
        Clone tree-sitter grammar repositories.
        """
        if not self.BUILD_DIR.exists():
            self.BUILD_DIR.mkdir()
        for language in tqdm(
            self.language_grammar_repos,
            total=len(self.language_grammar_repos),
            desc=f"Cloning grammar repositories for languages...",
        ):
            repo_url = self.language_grammar_repos[language]
            repo_path = self._get_repo_path(repo_url)
            if repo_path.exists():
                continue
            git.Repo.clone_from(repo_url, repo_path)

    def _get_repo_path(self, repo_url: str) -> Path:
        """
        Get path to cloned repository.
        :param repo_url: Repository URL.
        :return: Path to repository.
        """
        return self.BUILD_DIR / repo_url.split("/")[-1]

    def build_library(self) -> None:
        """
        Compile cloned grammar repositories into a library that's usable from Python.
        """
        grammar_repos_paths: List[str] = []

        for language in self.language_grammar_repos:
            repo_url = self.language_grammar_repos[language]
            repo_path = self._get_repo_path(repo_url)
            grammar_repos_paths.append(str(repo_path))
        Language.build_library(str(self.BUILD_LANGUAGES_PATH), grammar_repos_paths)

    def _get_parser(self, language: str) -> Parser:
        """
        Get language parser.
        :param language: Programming language.
        :return: Parser for given language.
        """
        parser = Parser()
        parser.set_language(self._get_language(language))
        return parser

    def _map_language_to_repo_language_name(self, language: str) -> str:
        """
        Map language name to tree-sitter repo language name.
        :param language: Programming language.
        :return: Language from tree-sitter.
        """
        repo_path = str(urlparse(self.language_grammar_repos[language]).path)
        return repo_path.split("-")[-1]

    def _get_language(self, language: str) -> Language:
        """
        Get language object from tree-sitter.
        :param language: Programming language.
        :return: Language object.
        """
        repo_language_name = self._map_language_to_repo_language_name(language)
        return Language(self.BUILD_LANGUAGES_PATH, repo_language_name)

    def can_parse(self, language: str) -> bool:
        """
        Determine whether it is possible to parse language.
        :param language: Programming language.
        :return: Can parse given language.
        """
        return language in self.language_grammar_repos

    def extract_with_tree_sitter(self, language: str, source_code: bytes) -> Counter:
        """
        Extract variable names from source code.
        :param language: Programming language.
        :param source_code: Content of file with code.
        :return: Variable names from source code with their frequencies.
        """
        identifiers = Counter()
        if not self.can_parse(language):
            return identifiers
        parser = self._get_parser(language)
        query = self._get_language(language).query(self.IDENTIFIERS_QUERY)
        captures = query.captures(parser.parse(source_code).root_node)
        for capture in captures:
            node = capture[0]
            identifier = source_code[node.start_byte : node.end_byte].decode()
            identifiers[identifier] += 1
        return identifiers
