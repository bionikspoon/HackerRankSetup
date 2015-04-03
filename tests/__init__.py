# coding=utf-8
from os.path import join

sample_url = ('https://www.hackerrank.com/'
              'challenges/sherlock-and-queries')
tests_directory = __path__[0]
sample_assets = lambda x: join(tests_directory, 'test_assets', x)

sample_config = sample_assets('repository_config.json')