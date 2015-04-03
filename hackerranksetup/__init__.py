# coding=utf-8
import logging
from os.path import join

directory_name = __path__[0]

logfile = join(directory_name, 'logs', 'hackerranksetup.log')
CONFIG_FILE = join(directory_name, 'config', 'config.json')
templates_path = join(directory_name, 'template')
LOGO = 'https://www.hackerrank.com/assets/brand/typemark_60x200.png'

logging.basicConfig(filename=logfile, filemode='a', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)

from challenge import Challenge
from repository import Repository

repo = Repository(CONFIG_FILE)

from teximage import TexImage
from utilities import ignored, publish_workspace
from frontpage import FrontPage
from readme import Readme