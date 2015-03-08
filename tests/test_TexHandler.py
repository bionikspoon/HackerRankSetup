# coding=utf-8
import filecmp
import tempfile
import unittest
import cPickle
import shutil
import os

import mock
import nose.tools as test

import hackerranksetup.TexHandler as HRTexHandler


root_directory = os.path.realpath(os.path.expanduser('~/code/HackerRankSetup'))


class TestTexHandler(unittest.TestCase):
    expected_assets = lambda *x: os.path.realpath(
        os.path.join(root_directory, 'tests/test_assets',
                     x[-1]))

    temp_dir = None
    tex_response = cPickle.load(open(expected_assets('tex_response.p'), 'rb'))
    sample_tex = '$B_1, B_2, \cdots, B_M$'

    @classmethod
    def setUpClass(cls):
        tempfile.tempdir = os.path.join(root_directory,
                                        'tests/.tmp')
        cls.temp_dir = tempfile.mkdtemp()
        cls.temp_assets = os.path.join(cls.temp_dir, 'test_assets')
        os.mkdir(cls.temp_assets)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)

    def setUp(self):
        patcher = mock.patch('hackerranksetup.TexHandler.requests')
        self.addCleanup(patcher.stop)
        self.mock_requests = patcher.start()
        self.mock_requests.get.return_value = self.tex_response
        assert HRTexHandler.requests is self.mock_requests

        self.tex = HRTexHandler.TexHandler(assets=self.temp_assets)

    def tearDown(self):
        pass

    def test_requests_properly_mocked(self):
        test.assert_equals(self.mock_requests, HRTexHandler.requests)

    def test_texhandler_initializes_properly(self):
        actual = os.path.realpath(self.tex.assets)
        expected = os.path.realpath(self.temp_assets)
        test.assert_equals(actual, expected)

        test.assert_equal(self.tex.assets, self.temp_assets)

    def test_get_returns_name_of_file(self):
        test.assert_equals(self.tex.get(self.sample_tex),
                           '931a66e3d5b402ced398785c46df78e4.png')

    def test_accurately_renders_png(self):
        actual = os.path.join(self.temp_assets, self.tex.get(self.sample_tex))
        expected = self.expected_assets('931a66e3d5b402ced398785c46df78e4.png')
        test.assert_true(filecmp.cmp(actual, expected))


if __name__ == '__main__':
    unittest.main()
