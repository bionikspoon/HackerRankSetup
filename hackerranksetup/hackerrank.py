# coding=utf-8
import logging
from os.path import join

import click

from hackerranksetup import (repo, templates_path, Challenge, FrontPage, Readme,
                             publish_workspace)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', '-d', is_flag=True, default=False,
              help='Turn debug mode on.')
def cli(debug):
    """HackerRank IDE setup utility."""

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('requests').setLevel(logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info('Debug On')


@cli.command()
@click.option('-f', '--force', is_flag=True, default=False)
@click.argument('url')
def new(url, force):
    """Setup new workspace."""
    if repo.current_challenge and not force:
        message = 'Workspace is in use.  Use -F or --force to override'
        raise click.ClickException(message)

    logging.info('new challenge:%s', url)

    repo.current_challenge = challenge = Challenge(url)
    Readme.save(challenge, repo.workspace, repo.assets)


@cli.command()
@click.option('-f', '--force', is_flag=True, default=False)
def publish(force):
    """Publish current puzzle."""

    if not repo.current_challenge:
        message = 'No current challenge to publish.'
        raise click.ClickException(message)

    logging.info('publishing current challenge')
    challenge = Challenge.from_repo(repo.current_challenge)

    destination = join(repo.root, challenge.path)

    publish_workspace(repo.workspace, destination, templates_path, force=force)

    logging.debug('Rebuilding readme at destination %s', destination)
    Readme.save(challenge, destination, repo.assets)
    FrontPage.save(repo.archive, repo.root)

    del repo.current_challenge


if __name__ == '__main__':
    cli()
