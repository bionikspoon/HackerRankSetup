# coding=utf-8
import ConfigParser
from os.path import join, dirname, realpath, expanduser


CONFIG_FILE = join(realpath(dirname(__name__)), 'config', 'config.cfg')


class Configuration(object):
    config = ConfigParser.SafeConfigParser()
    config.read(CONFIG_FILE)

    root = realpath(expanduser(config.get('HackerRank', 'Root')))
    workspace = realpath(expanduser(config.get('HackerRank', 'Workspace')))
    assets = realpath(expanduser(config.get('HackerRank', 'Assets')))


    @property
    def current(self):
        return Configuration.config.has_section('Current')

    @property
    def current_url(self):
        return Configuration.config.get('Current', 'url')

    @current_url.setter
    def current_url(self, url):
        try:
            Configuration.config.add_section('Current')
        except ConfigParser.DuplicateSectionError:
            pass

        Configuration.config.set('Current', 'url', url)
        with open(CONFIG_FILE, 'wb') as f:
            Configuration.config.write(f)

