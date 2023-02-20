import click
import json

from utils.repos_info_extractor import ReposInfoExtractor


@click.command()
def run():
    repos_list = ["https://github.com/ishepard/pydriller", "https://github.com/nolar/kopf"]

    info_extractor = ReposInfoExtractor(repos_list)
    programmers_info = info_extractor.get_programmers_commits_info()

    with open('programmers_commits.json', 'w') as fp:
        json.dump(programmers_info, fp, indent=4, sort_keys=True)


if __name__ == '__main__':
    run()
