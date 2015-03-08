# coding=utf-8
import click
import logging

logging.basicConfig(filename='hackerranksetup.log', filemode='w',
                    level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


@click.group()
def cli():
    click.echo('You made it!')


@cli.command()
@click.argument('url')
def load(url):
    logging.info('load:%s', url)
    click.echo('URL: {}'.format(url))


@cli.command()
def publish():
    click.echo('Publish!')

if __name__ == '__main__':
    cli()