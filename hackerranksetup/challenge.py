# coding=utf-8
import re

import requests


class Challenge(object):
    rest_base = (
        'https://www.hackerrank.com/rest/contests/master/challenges/')

    def __init__(self, url):
        self.url = url
        self._rest_endpoint = None
        self._model = None

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
            try:
                slug = re.compile('(?<=/)[a-z1-9-]+(?=/?)$')
                url_slug = slug.search(self.url).group()
            except AttributeError, e:
                url_invalid = "'NoneType' object has no attribute 'group'"
                error_message = 'Failed to get_rest_endpoint(%s)' % self.url
                raise ValueError(
                    error_message) if e.message == url_invalid else e
            else:
                self._rest_endpoint = self.rest_base + url_slug
        return self._rest_endpoint