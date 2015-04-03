# coding=utf-8
import logging
import shutil
from os.path import exists, isdir
from contextlib import contextmanager

import click


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def publish_workspace(workspace, destination, templates, force=False, ):
    """
    Check destination, delete if force.
    Move workspace.
    Delete Workspace
    Repopulate Workspace
    """
    if exists(destination) and not force:
        message = 'Destination already exists.  Use -F or --force to override'
        raise click.ClickException(message)
    else:
        # delete if force
        with ignored(OSError):
            shutil.rmtree(destination)
        # Move workspace.
        shutil.copytree(workspace, destination)
        logging.debug('copied workspace to destination %s', destination)
        # Delete Workspace
        if isdir(workspace):
            shutil.rmtree(workspace)
        # Repopulate workspace
        shutil.copytree(templates, workspace)
        logging.debug('copied template to file://%s', workspace)
