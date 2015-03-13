# coding=utf-8
import hashlib
import os

import requests
import click


class TexImage(object):
    api = 'http://chart.apis.google.com/chart'

    def __init__(self, assets='../test_assets/'):
        self.assets = os.path.realpath(assets)

    def get(self, tex):
        params = {'cht': 'tx', 'chs': 20, 'chl': tex}
        hash_id = hashlib.md5(tex).hexdigest()
        file_name = '{}.{}'.format(hash_id, 'png')
        file_path = os.path.join(self.assets, file_name)
        if not os.path.isfile(file_path):
            response = requests.get(self.api, params=params)
            with open(file_path, 'wb') as f:
                f.write(response.content)
        return file_name


@click.command()
@click.argument('assets', type=click.Path(exists=True))
@click.argument('tex', type=click.STRING)
def cli(assets, tex):
    click.echo(TexImage(assets).get(tex))


if __name__ == "__main__":
    cli()
    # _assets = '../test_assets/'
    # # _tex = raw_input('>>> ')
    # _tex = '$B_1, B_2, \cdots, B_M$'
    # tex_api = TexImage(assets=_assets)
    # print tex_api.get(_tex)