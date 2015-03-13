# coding=utf-8
import urllib
import codecs
import os.path
import re

import requests

from hackerranksetup.TexImage import TexImage


class Readme(object):
    rest_base = (
        'https://www.hackerrank.com/rest/contests/master/challenges/')
    hackerrank_logo = (
        'https://www.hackerrank.com/assets/brand/typemark_60x200.png')

    def __init__(self, url, workspace='../workspace/', assets='../assets/',
                 readme_file_name='README.md'):
        self.assets = os.path.realpath(assets)
        self.workspace = os.path.realpath(workspace)
        self.readme_file_name = readme_file_name

        self.url = url
        self._rest_endpoint = None
        self._model = None
        self._source = None
        self._readme = None
        self._source_file_name = None

    @property
    def model(self):
        if not self._model:
            response = requests.get(self.rest_endpoint)
            response.raise_for_status()
            self._model = response.json()['model']
        return self._model

    @property
    def source(self):
        if not self._source:
            model = self.model
            footnote = {'HackerRank': self.hackerrank_logo}
            logo = '![{0}]'.format('HackerRank')
            name = '#{}'.format(model['name'].strip())
            url_crumb = '{} \ {} \ {} \ {}'.format('HackerRank',
                                                   model['track']['track_name'],
                                                   model['track']['name'],
                                                   model['name'])
            link = '[{}]({})'.format(url_crumb, self.url)
            preview = '{}'.format(model['preview'])
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
            tex_api = TexImage(assets=self.assets)
            rel_assets = os.path.relpath(self.assets, self.workspace)
            footnote = {}

            def register_tex(match):
                match = match.group()
                tex_path = tex_api.get(match)
                match = match.replace('[', '').replace(']', '')
                footnote[match] = tex_path
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
            tex = re.compile(ur'\$[^$]+\$')
            readme = tex.sub(register_tex, readme)
            for k, v in footnote.iteritems():
                link = urllib.pathname2url(os.path.join(rel_assets, v))
                readme += '\n' + r'[{}]:{}'.format(k, link)
            self._readme = readme
        return self._readme

    @property
    def source_file_name(self):
        self._source_file_name = (
            self._source_file_name if self._source_file_name
            else '{}.md'.format(self.model['slug']))
        return self._source_file_name

    def save_source(self):
        with codecs.open(os.path.join(self.workspace, self.source_file_name),
                         'w', encoding='utf8') as f:
            f.write(self.source)
        return self

    def save_readme(self):
        with codecs.open(os.path.join(self.workspace, self.readme_file_name),
                         'w', encoding='utf8') as f:
            f.write(self.readme)
        return self

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

    def __str__(self):
        return self.readme.encode()


if __name__ == "__main__":
    _directory = '../proof_of_concept/'
    _assets = '../test_assets/'
    _url = raw_input('>>> ')
    print Readme(_url, workspace=_directory,
                 assets=_assets).save_source().save_readme()
