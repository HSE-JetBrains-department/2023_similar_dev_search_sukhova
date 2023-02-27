from pathlib import Path
from typing import List

import click
import io
import json

from utils.stargazers_top_extractor import StargazersTopExtractor
from utils.repos_info_extractor import ReposInfoExtractor


@click.command(name="prog")
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


@click.command("top")
@click.option("-r", "--repos_list", multiple=True, default=["https://github.com/pytorch/pytorch"],
              help="Provide paths to Github repositories.")
def stargazers_top(repos_list: List[str]) -> None:
    """
    Get top 100 GitHub repos in popularity among stargazers.
    Data is saved to results/repositories_top.json.

    :param repos_list: List of paths to GitHub repositories.
    """
    info_extractor = StargazersTopExtractor(repos_list)
    path_to_result = Path(__file__).parent.parent / "results" / "repositories_top.json"

    with open(path_to_result, "w") as fp:
        json.dump(info_extractor.repositories_top, fp, indent=8, sort_keys=True)


@click.command("top")
@click.option("-r", "--repos_list", multiple=True, default=["https://github.com/pytorch/pytorch"],
              help="Provide paths to Github repositories.")
def stargazers_top(repos_list: List[str]) -> None:
    """
    Get top 100 GitHub repos in popularity among stargazers.
    Data is saved to results/repositories_top.json.

    :param repos_list: List of paths to GitHub repositories.
    """
    info_extractor = StargazersTopExtractor(repos_list)
    path_to_result = Path(__file__).parent.parent / "results" / "repositories_top.json"

    with open(path_to_result, "w") as fp:
        json.dump(info_extractor.repositories_top, fp, indent=8, sort_keys=True)


@click.group()
def cli():
    """
    Similar developers search line tool.
    """


if __name__ == "__main__":
    cli.add_command(programmers_info)
    cli.add_command(stargazers_top)
    cli()
