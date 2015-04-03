# coding=utf-8
from contextlib import contextmanager
from functools import wraps
import json
import logging
from os.path import exists, isdir
import shutil
import click
from . import repo


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


def save_config(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            json.dump(repo.data, open(repo.config_file, 'w'), indent=2,
                      sort_keys=True, separators=(',', ': '))
    return wrapper