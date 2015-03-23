# coding=utf-8
import logging
import shutil
from os.path import join, dirname, isdir, exists

import click

from hackerranksetup.repository import Repository
from hackerranksetup.challenge import Challenge
from hackerranksetup.readme import Readme
from hackerranksetup.tableofcontents import TableOfContents
from hackerranksetup.utilities import ignored


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', '-D', is_flag=True, default=False,
              help='Turn debug mode on.')
@click.pass_context
def cli(ctx, debug):
    """HackerRank IDE setup utility."""

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('requests').setLevel(logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info('Debug On')

    ctx.obj = Repository()


@cli.command()
@click.option('-F', '--force', is_flag=True, default=False)
@click.argument('url')
@click.pass_context
def new(ctx, url, force):
    """Setup new workspace."""
    if ctx.obj.current_challenge and not force:
        message = 'Workspace is in use.  Use -F or --force to override'
        raise click.ClickException(message)

    logging.info('new:%s', url)
    logging.debug('ctx.obj:%s', ctx.obj)

    ctx.obj.current_challenge = challenge = Challenge(url)
    Readme(challenge, ctx.obj.workspace, ctx.obj.assets).save()


@cli.command()
@click.option('-F', '--force', is_flag=True, default=False)
@click.pass_context
def publish(ctx, force):
    """Publish current puzzle."""
    logging.info('publish')
    logging.debug('ctx.obj:%s', ctx.obj)

    challenge = Challenge(ctx.obj.current_challenge)

    destination = join(ctx.obj.root, challenge.path)
    if exists(destination) and not force:
        raise click.ClickException(
            'Destination already exists.  Use -F or --force to override')
    else:
        with ignored(OSError):
            shutil.rmtree(destination, ignore_errors=True)

    shutil.copytree(ctx.obj.workspace, destination)
    logging.debug('copied workspace to destination %s', destination)
    Readme(challenge, destination, ctx.obj.assets).save()
    logging.debug('Rebuilt readme at destination %s', destination)

    ctx.obj.archive_challenge(challenge)

    TableOfContents(ctx.obj.archive, ctx.obj.root).save()

    template_directory = join(dirname(__file__), 'template')
    if isdir(ctx.obj.workspace):
        shutil.rmtree(ctx.obj.workspace)
    shutil.copytree(template_directory, ctx.obj.workspace)
    logging.debug('copied template to file://%s', ctx.obj.workspace)


if __name__ == '__main__':
    cli()
