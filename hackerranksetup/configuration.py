# coding=utf-8
import json
from os.path import join, dirname, realpath


CONFIG_FILE = join(realpath(dirname(__name__)), 'config', 'config.json')


class Configuration(object):
    config = json.load(open(CONFIG_FILE))

    root = config['HackerRank']['root']
    workspace = config['HackerRank']['workspace']
    assets = config['HackerRank']['assets']

    @property
    def current(self):
        return Configuration.config.get('Current')

    @property
    def current_url(self):
        return Configuration.config.get('Current').get('url')

    @current_url.setter
    def current_url(self, url):
        if not Configuration.config.get('Current'):
            Configuration.config['Current'] = {}
        Configuration.config['Current']['url'] = url
        Configuration.save()

    @staticmethod
    def reset():
        del Configuration.config['Current']

        Configuration.save()

    @staticmethod
    def save():
        json.dump(Configuration.config, open(CONFIG_FILE, 'w'), indent=2,
                  sort_keys=True)

    @property
    def table_of_contents(self):
        return Configuration.config.get('Table of Contents')

    @table_of_contents.setter
    def table_of_contents(self, challenge):
        model = challenge.model
        track_name = model['track']['track_name']
        track = model['track']['name']
        name = model['name']
        path = join(model['track']['track_slug'], model['track']['slug'],
                    model['slug'])
        url = '{}{}'.format('https://www.hackerrank.com/challenges/',
                            model['slug'])

        if not Configuration.config.get('Table of Contents'):
            Configuration.config['Table of Contents'] = {}
        toc = Configuration.config['Table of Contents']

        if not toc.get(track_name):
            toc[track_name] = {}

        if not toc.get(track_name).get(track):
            toc[track_name][track] = {}

        challenge = toc[track_name][track][name] = {}
        challenge['url'] = url
        challenge['path'] = path

        Configuration.save()