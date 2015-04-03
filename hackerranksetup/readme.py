# coding=utf-8
import os
import re
import urllib

from . import TexImage, LOGO


class Readme(object):
    def __init__(self, challenge, destination, assets, tex_image=TexImage):
        self.challenge = challenge
        self.destination = destination
        self.assets = assets
        self.tex = tex_image(assets)
        self._source = None
        self._readme = None

    @classmethod
    def save(cls, *args, **kwargs):
        self = cls(*args, **kwargs)

        filename = os.path.join(self.destination, 'README.md')
        with open(filename, 'w') as f:
            f.write(self.readme)
        return self

    @property
    def source(self):
        if not self._source:
            challenge = self.challenge
            logo = '![{0}]'.format('HackerRank')
            name = '#{}'.format(challenge.name)
            link = '[{}]({})'.format(challenge.url_crumb('{} \ {} \ {} \ {}'),
                                     challenge.url)

            body = ('\n##{}\n{}'.format('Problem Statement',
                                        challenge.problem_statement))
            footnote = '\n[{}]:{}'.format('HackerRank', LOGO)

            source = '\n'.join(
                [logo, name, link, challenge.preview, body, footnote])

            source = re.compile(' +$', re.M).sub('', source)
            source = re.compile('\t').sub('    ', source)
            self._source = source
        return self._source

    @property
    def readme(self):
        if not self._readme:
            relpath_assets = os.path.relpath(self.assets, self.destination)
            footnote = {}

            def register_tex(match):
                match = match.group()
                tex_filename = self.tex.get(match)

                match = match.replace('[', '').replace(']', '').replace('\\',
                                                                        '')
                footnote[match] = tex_filename
                return '![{}]'.format(match)

            readme = self.source
            h3 = re.compile('^\*\*([\w ?]+)\*\*$', re.M)
            readme = h3.sub(r'###\1', readme)
            newline = ('(```)([^`]*?)(?(2)(```))'
                       '|(?:(?:\n?(?: {4,})+.*\n)+\n?)'
                       '|(?P<space>(?<!\n)\n(?!\n))')
            replacement = lambda x: "\n\n" if x.group('space') else x.group()
            readme = re.compile(newline).sub(replacement, readme)
            tex_search = re.compile('\$[^$]+\$')
            readme = tex_search.sub(register_tex, readme)

            for k, v in footnote.iteritems():
                link = urllib.pathname2url(os.path.join(relpath_assets, v))
                readme += '\n[{}]:{}'.format(k, link)
            self._readme = readme
        return self._readme