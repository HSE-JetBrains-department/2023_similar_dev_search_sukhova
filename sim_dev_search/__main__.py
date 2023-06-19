from pathlib import Path
import sys
from typing import List, Optional

import click
import json

from sim_dev_search.processors.repos_info_extractor import ReposInfoExtractor
from sim_dev_search.processors.sim_dev_finder import SimilarDevelopersFinder
from sim_dev_search.processors.stargazers_top_extractor import StargazersTopExtractor


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
    "-f",
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


@cli.command("sim_dev")
@click.option(
    "-u",
    "--user-email",
    required=True,
    help="Email of developer to find similar.",
)
@click.option(
    "-i",
    "--in-file-path",
    default=str(Path(__file__).absolute().parent.parent / "results" / "programmers_commits.json"),
    type=click.Path(file_okay=True, dir_okay=False),
    help="Path to file with information about developers.",
)
@click.option(
    "-o",
    "--out-file-path",
    required=False,
    type=click.Path(file_okay=True, dir_okay=False),
    help="Path to file with information about developers.",
)
def find_similar_developers(user_email: str, in_file_path: str, out_file_path: str) -> None:
    """
    Find similar to given developer.
    :param user_email: Email of developer to find similar.
    :param in_file_path: Path to file with information about developers.
    :param out_file_path: Path to file with results.
    """
    in_file_path_absolute = Path(in_file_path).absolute()
    try:
        with open(in_file_path_absolute, "r", encoding="utf-8") as file_in:
            developers_info = json.load(file_in)
    except (json.decoder.JSONDecodeError, FileNotFoundError) as exc:
        print(f"Exception while getting json from {in_file_path_absolute}: {exc}", file=sys.stderr)
        return
    if user_email not in developers_info:
        print(f"Can not find developer {user_email} in developers info!", file=sys.stderr)
        return
    sim_dev_info = SimilarDevelopersFinder().get_similar_developers(user_email, developers_info)
    if out_file_path:
        out_file_path_absolute = Path(in_file_path).absolute()
    else:
        out_file_path_absolute = str(
            Path(__file__).absolute().parent.parent / "results" / f"similar_developers_for_{user_email}.json"
        )
    with open(out_file_path_absolute, "w", encoding="utf-8") as file_out:
        json.dump(sim_dev_info, file_out, indent=4)
    print(f"Similar developers information has been saved to {out_file_path_absolute}.")


if __name__ == "__main__":
    cli()
