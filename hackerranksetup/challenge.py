# coding=utf-8
import os.path
import re

import requests


class Challenge(object):
    rest_base = ('https://www.hackerrank.com/rest/'
                 'contests/master/challenges/')
    url_base = 'https://www.hackerrank.com/challenges/'
    find_slug = re.compile('(?<=/)[a-z1-9-]+(?=/?)$')

    def __init__(self, url, model=None):
        self._url = None
        self._rest_endpoint = None
        self._model = model
        self.url = url

    @property
    def model(self):
        if not self._model:
            response = requests.get(self.rest_endpoint)
            response.raise_for_status()
            self._model = response.json()['model']
        return self._model

    @property
    def rest_endpoint(self):
        if not self._rest_endpoint:
            slug = self.find_slug.search(self.url)
            self._rest_endpoint = self.rest_base + slug.group()
        return self._rest_endpoint

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        slug = self.find_slug.search(value)
        if not slug:
            raise ValueError('URL or slug required')
        self._url = self.url_base + slug.group()

    @property
    def path(self):
        return os.path.join(self.model['track']['track_slug'],
                            self.model['track']['slug'], self.model['slug'])