# coding=utf-8
import hashlib
import os.path
import re
import urllib
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


class Readme(object):
    hackerrank_logo = (
        'https://www.hackerrank.com/assets/brand/typemark_60x200.png')

    def __init__(self, challenge, destination, assets, source=None):
        self.challenge = challenge
        self.destination = destination
        self.assets = assets
        self._source = source
        self._readme = None

    def save(self):
        filename = os.path.join(self.destination, 'README.md')
        with open(filename, 'w') as f:
            f.write(self.readme)
        return self

    @property
    def source(self):
        if not self._source:
            model = self.challenge.model
            footnote = {'HackerRank': self.hackerrank_logo}
            logo = '![{0}]'.format('HackerRank')
            name = '#{}'.format(model['name'].strip())
            url_crumb = '{} \ {} \ {} \ {}'.format('HackerRank',
                                                   model['track']['track_name'],
                                                   model['track']['name'],
                                                   model['name'])
            link = '[{}]({})'.format(url_crumb, self.challenge.url)
            model_preview = model['preview'] if model['preview'] else ''
            preview = '{}'.format(model_preview)
            body = (u'\n##{}\n{}'.format('Problem Statement', model['_data'][
                'problem_statement'].strip()))
            footnote = '\n[{}]:{}'.format('HackerRank', footnote['HackerRank'])

            source = u'\n'.join([logo, name, link, preview, body, footnote])

            source = re.compile(r' +$', re.M).sub('', source)
            source = re.compile(ur'\t', re.U).sub(u'    ', source)
            self._source = source
        return self._source

    @property
    def readme(self):
        if not self._readme:
            tex = TexImage(self.assets)
            relpath_assets = os.path.relpath(self.assets, self.destination)
            footnote = {}

            def register_tex(match):
                match = match.group()
                tex_filename = tex.get(match)
                match = match.replace('[', '').replace(']', '')
                footnote[match] = tex_filename
                return '![{}]'.format(match)

            readme = self.source
            h3 = re.compile(ur'^\*\*([\w ?]+)\*\*$', re.M)
            readme = h3.sub(ur'###\1', readme)
            newline = (
                ur'(```)([^`]*?)(?(2)(```))'
                ur'|(?:(?:\n?(?: {4,})+.*\n)+\n?)'
                ur'|(?P<space>(?<!\n)\n(?!\n))')
            repl = lambda x: "\n\n" if x.group('space') else x.group()
            readme = re.compile(newline).sub(repl, readme)
            tex_search = re.compile(ur'\$[^$]+\$')
            readme = tex_search.sub(register_tex, readme)
            for k, v in footnote.iteritems():
                link = urllib.pathname2url(os.path.join(relpath_assets, v))
                readme += '\n' + r'[{}]:{}'.format(k, link)
            self._readme = readme
        return self._readme


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
                slug = re.compile(ur'(?<=/)[a-z1-9-]+(?=/?)$')
                url_slug = slug.search(self.url).group()
            except AttributeError, e:
                url_invalid = "'NoneType' object has no attribute 'group'"
                error_message = 'Failed to get_rest_endpoint(%s)' % self.url
                raise ValueError(
                    error_message) if e.message == url_invalid else e
            else:
                self._rest_endpoint = self.rest_base + url_slug
        return self._rest_endpoint


class Workspace(object):
    def __init__(self, root, workspace, assets):
        self.root = root
        self.workspace = workspace
        self.assets = assets

    def new(self, url):
        challenge = Challenge(url)
        readme = Readme(challenge, self.workspace, self.assets)
        readme.save()

    def publish(self):
        pass
