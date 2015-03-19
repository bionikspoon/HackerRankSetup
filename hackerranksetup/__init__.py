# coding=utf-8
import logging
from os.path import join, dirname

logfile = join(dirname(__file__), 'logs', 'hackerranksetup.log')

logging.basicConfig(filename=logfile, filemode='a', level=logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)