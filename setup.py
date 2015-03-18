# coding=utf-8
from setuptools import setup, find_packages

setup(name='HackerRankSetup',
      version='0.1',
      license='MIT',
      description='Coming Soon',
      long_description='''
      Coming Soon
      ''',
      author='Manu Phatak',
      url='https://github.com/bionikspoon/HackerRankSetup',
      author_email='bionikspoon@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['click', 'mock', 'requests', 'pytest'],
      package_data={'hackerranksetup': ['config/config.cfg']},
      platforms=["Linux"],
      entry_points={
          'console_scripts': ['hackerrank = hackerranksetup.hackerrank:cli']
      },)