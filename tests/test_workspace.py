# coding=utf-8
import tempfile
import unittest
import shutil
import os.path

import pytest


pytestmark = pytest.mark.skipif(True, reason='Depreciated')

root_directory = os.path.dirname(os.path.dirname(__file__))
expected_assets = lambda x: os.path.realpath(
    os.path.join(root_directory, 'tests/test_assets', x))


class TestWorkspace(unittest.TestCase):
    _temp_dir = None

    @classmethod
    def setUpClass(cls):
        tempfile.tempdir = os.path.realpath(
            os.path.join(root_directory, 'tests/.tmp'))
        cls._temp_dir = tempfile.mkdtemp()
        cls.assets = os.path.realpath(os.path.join(root_directory, 'assets'))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls._temp_dir):
            shutil.rmtree(cls._temp_dir)


if __name__ == '__main__':
    unittest.main()
