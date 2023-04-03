from pathlib import Path
from typing import List

import click
import json

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


@click.group()
def cli():
    """
    Similar developers search line tool.
    """


if __name__ == "__main__":
    cli.add_command(programmers_info)
    cli()
