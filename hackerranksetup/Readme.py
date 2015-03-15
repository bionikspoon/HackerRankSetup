# coding=utf-8
import os
import re
import urllib

from hackerranksetup import TexImage


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
            tex = TexImage.TexImage(self.assets)
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