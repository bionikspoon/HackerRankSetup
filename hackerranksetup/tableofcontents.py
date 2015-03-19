# coding=utf-8
import json
from os.path import dirname, relpath, join
import urllib


class TableOfContents(object):
    hackerrank_logo = ('https://www.hackerrank.com'
                       '/assets/brand/typemark_60x200.png')

    def __init__(self, toc, root):
        self.toc = toc
        self.root = root

    @property
    def tableofcontents(self):
        toc = self.toc
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

    def save(self):
        footnote = {'HackerRank': TableOfContents.hackerrank_logo}
        logo = '![{0}]'.format('HackerRank')
        name = '#{}'.format('Table of contents')

        toc = self.tableofcontents
        footnote = '\n[{}]:{}'.format('HackerRank', footnote['HackerRank'])

        readme = '\n'.join([logo, name, toc, footnote])
        print readme
        with open(join(self.root, 'README.md'), 'w') as f:
            f.write(readme)


if __name__ == '__main__':
    toc_ = (
        '{"Algorithms": '
        '{"Summations and Algebra": '
        '{"Sherlock and Queries": '
        '{"path": "algorithms/summations-and-algebra/sherlock-and-queries", '
        '"url": "https://www.hackerrank.com/challenges/sherlock-and-queries"'
        '}}}}')
    TableOfContents(json.loads(toc_), dirname(__file__)).save()
