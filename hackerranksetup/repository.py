# coding=utf-8
import collections
from functools import wraps
from os.path import join, dirname, realpath
import json

config_tree = lambda: DefaultDictWithSave(config_tree)


def save_config(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            Repository.save_config()

    return wrapper


class DefaultDictWithSave(collections.defaultdict):
    @save_config
    def __setitem__(self, key, value):
        super(DefaultDictWithSave, self).__setitem__(key, value)

    @save_config
    def __delitem__(self, key):
        super(DefaultDictWithSave, self).__delitem__(key)


class Repository(collections.MutableMapping):
    CONFIG_FILE = join(realpath(dirname(__name__)), 'config', 'config.json')
    data = config_tree()

    def __init__(self):
        Repository.data = config_tree()
        Repository.data.update(json.load(open(Repository.CONFIG_FILE)))

    def __getitem__(self, item):
        return Repository.data.__getitem__(item)

    @save_config
    def __setitem__(self, key, value):
        Repository.data.__setitem__(key, value)

    @save_config
    def __delitem__(self, key):
        Repository.data.__delitem__(key)

    def __len__(self):
        return Repository.data.__len__()

    def __iter__(self):
        return Repository.data.__iter__()

    def __str__(self):
        return str(dict(Repository.data))

    @property
    def current_challenge(self):
        return self.get('Current')

    @current_challenge.setter
    def current_challenge(self, challenge):
        self['Current']['url'] = challenge.url
        self['Current']['path'] = challenge.path
        self['Current']['model'] = challenge.model

    @current_challenge.deleter
    def current_challenge(self):
        del self['Current']

    def archive_challenge(self, challenge):
        del self['Current']

        model = challenge.model

        track_name = model['track']['track_name']
        track = model['track']['name']
        name = model['name']
        path = challenge.path
        url = challenge.url

        self['Archive'][track_name][track][name]['url'] = url
        self['Archive'][track_name][track][name]['path'] = path

    @staticmethod
    def save_config():
        json.dump(Repository.data, open(Repository.CONFIG_FILE, 'w'), indent=2,
                  sort_keys=True, separators=(',', ': '))
