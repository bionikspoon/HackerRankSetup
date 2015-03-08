# coding=utf-8
import hashlib
import os

import requests


class TexHandler(object):
    api = 'http://chart.apis.google.com/chart'

    def __init__(self, assets='../test_assets/'):
        self.assets = os.path.realpath(assets)

    def get(self, tex):
        params = {'cht': 'tx', 'chs': 20, 'chl': tex}
        hash_id = hashlib.md5(tex).hexdigest()
        file_name = '{}.{}'.format(hash_id, 'png')
        file_path = os.path.join(self.assets, file_name)
        response = requests.get(self.api, params=params)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_name


if __name__ == "__main__":
    _assets = '../test_assets/'
    # _tex = raw_input('>>> ')
    _tex = '$B_1, B_2, \cdots, B_M$'
    tex_api = TexHandler(assets=_assets)
    print tex_api.get(_tex)