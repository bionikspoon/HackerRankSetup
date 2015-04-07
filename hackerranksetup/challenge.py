# coding=utf-8
import codecs
from os.path import join
import re

import requests


class Challenge(object):
    rest_base = ('https://www.hackerrank.com/rest/'
                 'contests/master/challenges/')
    url_base = 'https://www.hackerrank.com/challenges/'
    find_slug = re.compile('(?<=/)[a-z1-9-]+(?=/?)$')

    _challenge_map = None

    def __init__(self, url, model=None, requests=requests):
        self._url = None
        self._rest_endpoint = None
        self.requests = requests
        self._model = model
        self.url = url

    @classmethod
    def from_repo(cls, challenge, *args, **kwargs):
        self = cls(challenge['url'], challenge, *args, **kwargs)
        return self

    def __getattr__(self, item):
        return self.challenge_map.get(item)

    @property
    def challenge_map(self):
        if not self._challenge_map:
            model = self.model
            data = {'name': model['name'].strip(),
                    'preview': model['preview'] if model['preview'] else '',
                    'problem_statement': codecs.encode(
                        model['_data']['problem_statement'], 'utf-8').strip(),
                    'path': join(model['track']['track_slug'],
                                 model['track']['slug'], model['slug']),
                    'track_main': model['track']['track_name'],
                    'track_sub': model['track']['name'],
                    'slug': model['slug']}
            self._challenge_map = data
        return self._challenge_map

    @property
    def model(self):
        if not self._model:
            response = self.requests.get(self.rest_endpoint)
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

    def url_crumb(self, template='{} \ {} \ {} \ {}'):
        model = self.model
        return template.format('HackerRank', model['track']['track_name'],
                               model['track']['name'], model['name'])

    def json(self):
        model = self.model
        model['url'] = self.url
        return self.model
