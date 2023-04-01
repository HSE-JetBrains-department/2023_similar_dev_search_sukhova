from pathlib import Path
from typing import List

import json
import click
import io

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
    "--file-out",
    default=click.open_file(str(Path(__file__).absolute().parent.parent / "results" / "programmers_commits.json"), "w"),
    type=click.File("w"),
    help="Provide path to save result.",
)
def programmers_info(repos_list: List[str], file_out: io.TextIOWrapper) -> None:
    """
    Get information about developers and their commits.

    :param repos_list: List of paths to GitHub repositories.
    :param file_out: file to write results.
    """
    info_extractor = ReposInfoExtractor(repos_list)
    json.dump(info_extractor.programmers_info, file_out, indent=8, sort_keys=True)


@click.group()
def cli():
    """
    Similar developers search line tool.
    """


if __name__ == "__main__":
    cli.add_command(programmers_info)
    cli()
