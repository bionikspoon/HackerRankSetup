# coding=utf-8
from setuptools import setup, find_packages

setup(name='HackerRankSetup',
      version='0.1',
      license='MIT',
      description='',
      long_description='',
      author='Manu Phatak',
      url='',
      author_email='bionikspoon@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['click'],
      entry_points="""
      [console_scripts]
      hackerrank=hackerrank:cli
      """,
      )