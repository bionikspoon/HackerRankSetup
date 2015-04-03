# coding=utf-8
import json

from . import Challenge, save_config


class Repository(object):
    data = None

    def __init__(self, config_file, challenge=Challenge):
        self.config_file = config_file
        self.data = json.load(open(self.config_file))
        self.Challenge = challenge

    @property
    def root(self):
        return self.data['Directory']['root']

    @property
    def assets(self):
        return self.data['Directory']['assets']

    @property
    def workspace(self):
        return self.data['Directory']['workspace']

    @property
    def current_challenge(self):
        return self.data.get('Current')

    @current_challenge.setter
    @save_config
    def current_challenge(self, challenge):
        self.data['Current'] = dict(challenge)

    @current_challenge.deleter
    @save_config
    def current_challenge(self):
        c = self.Challenge.from_repo(self.data['Current'])

        if not self.data.get('Archive'):
            self.data['Archive'] = {}

        if not self.data['Archive'].get(c.track_main):
            self.data['Archive'][c.track_main] = {}

        if not self.data['Archive'][c.track_main].get(c.track_sub):
            self.data['Archive'][c.track_main][c.track_sub] = {}

        if not self.data['Archive'][c.track_main][c.track_sub].get(c.name):
            self.data['Archive'][c.track_main][c.track_sub][c.name] = {}

        self.data['Archive'][c.track_main][c.track_sub][c.name]['url'] = c.url
        self.data['Archive'][c.track_main][c.track_sub][c.name]['path'] = c.path

        del self.data['Current']

    @property
    def archive(self):
        return self.data.get('Archive')
