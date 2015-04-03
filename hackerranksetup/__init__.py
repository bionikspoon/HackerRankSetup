# coding=utf-8
import logging
from os.path import join, dirname, realpath
from .repository import Repository
from .challenge import Challenge
from .readme import Readme
from .frontpage import FrontPage
from .utilities import ignored, publish_workspace, save_config
from .teximage import TexImage

logfile = join(dirname(__file__), 'logs', 'hackerranksetup.log')
CONFIG_FILE = join(realpath(dirname(__name__)), 'config', 'config.json')
templates_path = join(dirname(__file__), 'template')
LOGO = 'https://www.hackerrank.com/assets/brand/typemark_60x200.png'

logging.basicConfig(filename=logfile, filemode='a', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)

repo = Repository(CONFIG_FILE)
