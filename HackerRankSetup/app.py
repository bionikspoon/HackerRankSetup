# coding=utf-8
import ConfigParser
import os

import HackerRankSetup.HackerRankReadme


config = ConfigParser.SafeConfigParser()
config.read('config.cfg')

root = os.path.realpath(os.path.expanduser(config.get('HackerRank', 'Root')))

workspace = os.path.realpath(
    os.path.expanduser(config.get('HackerRank', 'Workspace')))
assets = os.path.realpath(
    os.path.expanduser(config.get('HackerRank', 'Assets')))

url = 'https://www.hackerrank.com/challenges/sherlock-and-queries'

print HackerRankSetup.HackerRankReadme.HackerRankReadme(url, root=root,
                                                        workspace=workspace,
                                                        assets=assets).run()