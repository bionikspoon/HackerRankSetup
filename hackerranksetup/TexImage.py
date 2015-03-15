# coding=utf-8
import hashlib
import os

import requests


class TexImage(object):
    url_endpoint = 'http://chart.apis.google.com/chart'

    def __init__(self, assets):
        self.assets = assets

    def get(self, code):
        hash_id = hashlib.md5(code).hexdigest()
        file_name = '{}.{}'.format(hash_id, 'png')
        file_path = os.path.join(self.assets, file_name)
        if not os.path.isfile(file_path):
            self.save(code, file_path)
        return file_name

    def save(self, code, file_path):
        params = {'cht': 'tx', 'chs': 20, 'chl': code}
        response = requests.get(self.url_endpoint, params=params)
        with open(file_path, 'wb') as f:
            f.write(response.content)