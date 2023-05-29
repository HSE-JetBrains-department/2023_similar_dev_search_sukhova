from pathlib import Path
from typing import List, Optional

import click
import json

from utils.stargazers_top_extractor import StargazersTopExtractor
from utils.repos_info_extractor import ReposInfoExtractor


@click.group()
def cli():
    """
    Similar developers search line tool.
    """


@cli.command(name="prog")
@click.option(
    "-r",
    "--repos_list",
    multiple=True,
    default=["https://github.com/ishepard/pydriller"],
    help="Provide paths to Github repositories.",
)
@click.option(
    "-p",
    "--file-path",
    default=str(Path(__file__).absolute().parent.parent / "results" / "programmers_commits.json"),
    type=click.Path(file_okay=True, dir_okay=False),
    help="Provide path to save result.",
)
def programmers_info(repos_list: List[str], file_path: str) -> None:
    """
    Get information about developers and their commits.
    :param repos_list: List of paths to GitHub repositories.
    :param file_path: Path to file with results.
    """
    file_path_absolute = Path(file_path).absolute()
    info_extractor = ReposInfoExtractor(repos_list)

    with open(file_path_absolute, "w", encoding="utf-8") as file_out:
        json.dump(info_extractor.programmers_info, file_out, indent=4, sort_keys=True)


@cli.command("top")
@click.option(
    "-r",
    "--repos_list",
    multiple=True,
    default=["https://github.com/pytorch/pytorch"],
    help="Provide paths to Github repositories.",
)
@click.option(
    "-f",
    "--file-path",
    default=str(Path(__file__).absolute().parent.parent / "results" / "repositories_top.json"),
    type=click.Path(file_okay=True, dir_okay=False),
    help="Provide path to save result.",
)
@click.option(
    "-a",
    "--api-token",
    default=None,
    help="Github API access token.",
)
def stargazers_top(repos_list: List[str], file_path: str, api_token: Optional[str]) -> None:
    """
    Get top 100 GitHub repos in popularity among stargazers.
    :param repos_list: List of paths to GitHub repositories.
    :param file_path: Path to file with results.
    :param api_token: API access token.
    """
    file_path_absolute = Path(file_path).absolute()
    info_extractor = StargazersTopExtractor(repos_list, api_token)

    with open(file_path_absolute, "w", encoding="utf-8") as file_out:
        json.dump(info_extractor.repositories_top, file_out, indent=4)


if __name__ == "__main__":
    cli()
