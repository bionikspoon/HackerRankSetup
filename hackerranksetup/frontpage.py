# coding=utf-8
import json
from os.path import dirname, relpath, join
import urllib
from . import LOGO


class FrontPage(object):
    def __init__(self, archive, root):
        self.archive = archive
        self.root = root

    @classmethod
    def save(cls, *args, **kwargs):
        self = cls(*args, **kwargs)

        source = self.source
        with open(join(self.root, 'README.md'), 'w') as f:
            f.write(source)
        return self

    @property
    def table_of_contents(self):
        toc = self.archive
        result = ''
        for track_k, track_v in toc.items():
            result += '\n### {}'.format(track_k)
            for sub_track_k, sub_track_v in track_v.items():
                result += '\n- {}'.format(sub_track_k)
                for challenge_name, model in sub_track_v.items():
                    link = relpath(join(self.root, model['path']), self.root)
                    link = urllib.pathname2url(link)
                    result += '\n  - [x] [{}]({})'.format(challenge_name, link)

        return result

    @property
    def source(self):
        footnote = {'HackerRank': LOGO}
        logo = '![{0}]'.format('HackerRank')
        name = '#{}'.format('Table of contents')

        footnote = '\n[{}]:{}'.format('HackerRank', footnote['HackerRank'])

        return '\n'.join([logo, name, self.table_of_contents, footnote])


if __name__ == '__main__':
    toc_ = ('{"Algorithms": '
            '{"Summations and Algebra": '
            '{"Sherlock and Queries": '
            '{"path": "algorithms/summations-and-algebra/sherlock-and-queries'
            '", '
            '"url": "https://www.hackerrank.com/challenges/sherlock-and'
            '-queries"'
            '}}}}')
    FrontPage(json.loads(toc_), dirname(__file__)).save()
