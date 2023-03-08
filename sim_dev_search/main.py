from typing import List

import click
import json

from utils.repos_info_extractor import ReposInfoExtractor


@click.command()
@click.option("-r", "--repos_list", multiple=True, default=["https://github.com/ishepard/pydriller"],
              help="Provide paths to Github repositories.")
def run(repos_list: List[str]) -> None:
    """

    :param repos_list:
    :return:
    """
    info_extractor = ReposInfoExtractor(repos_list)
    path_to_result = 'results/programmers_commits.json'

    with open(path_to_result, 'w') as fp:
        json.dump(info_extractor.programmers_info, fp, indent=8, sort_keys=True)


if __name__ == '__main__':
    run()
