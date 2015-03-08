# coding=utf-8
import difflib
import tempfile
import unittest
import json
import cPickle
import shutil
import os.path

import mock
import nose.tools as test

import HackerRankSetup.HackerRankReadme as HRReadme


root_directory = os.path.realpath(os.path.expanduser('~/code/HackerRank'))


class TestHackerRankReadme(unittest.TestCase):
    test_assets = lambda *x: os.path.realpath(
        os.path.join(root_directory, 'HackerRankSetup/tests/test_assets',
                     x[-1]))

    with open(test_assets('hackerrank_response.p'), 'rb') as response:
        hackerrank_response = cPickle.load(response)
    with open(test_assets('mock_tex_response.json')) as response:
        tex_response = json.load(response)
    test_url = ('https://www.hackerrank.com/'
                'challenges/sherlock-and-queries')
    root = os.path.realpath('./')
    _temp_dir = None

    @classmethod
    def setUpClass(cls):
        tempfile.tempdir = os.path.realpath(
            os.path.join(root_directory, 'HackerRankSetup/tests/.tmp'))
        cls._temp_dir = tempfile.mkdtemp()
        cls.assets = os.path.realpath(os.path.join(root_directory, 'assets'))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls._temp_dir):
            shutil.rmtree(cls._temp_dir)

    def setUp(self):
        self.handler = HRReadme.HackerRankReadme(self.test_url, root=self.root,
                                                 workspace=self._temp_dir,
                                                 assets=self.assets)

        th_patcher = mock.patch('HackerRankSetup.HackerRankReadme.TexHandler')
        self.MockTexHandler = th_patcher.start()
        self.addCleanup(th_patcher.stop)
        test_tex = self.MockTexHandler.return_value
        test_tex.get.side_effect = self.tex_response.get
        assert HRReadme.TexHandler is self.MockTexHandler

        rq_patcher = mock.patch('HackerRankSetup.HackerRankReadme.requests')
        self.addCleanup(rq_patcher.stop)
        self.MockRequests = rq_patcher.start()
        self.MockRequests.get.return_value = self.hackerrank_response
        assert HRReadme.requests is self.MockRequests

    def tearDown(self):
        del self.handler

    def test_class_initializes_properly(self):
        test.assert_equals(os.path.realpath(self.handler._workspace),
                           os.path.realpath(self._temp_dir))
        test.assert_equals(self.handler.url, self.test_url)
        rest_endpoint = ('https://www.hackerrank.com/'
                         'rest/contests/master/challenges/sherlock-and-queries')
        test.assert_equals(self.handler.rest_endpoint, rest_endpoint)
        test.assert_equals(self.handler.readme_file_name, 'README.md')
        test.assert_is_none(self.handler._model)
        test.assert_is_none(self.handler._source)
        test.assert_is_none(self.handler._readme)
        test.assert_is_none(self.handler._source_file_name)
        # test.assert_false(os.path.exists(self.temp_dir))

    def test_correct_file_name_for_source(self):
        test.assert_equals(self.handler.source_file_name,
                           'sherlock-and-queries.md')

    def test_build_source(self):
        source_file = self.test_assets('sherlock-and-queries.md')
        with open(source_file) as source_file:
            source = self.handler.build_source()
            print source
            expected = source_file.read()
            test.assert_equals(source, expected, self.diff(source, expected))

    def test_build_readme(self):
        with open(self.test_assets('README.md')) as readme_file:
            readme = self.handler.build_readme()
            # print readme
            expected = readme_file.read()
            test.assert_equals(readme, expected, self.diff(readme, expected))

    def test_run_creates_source(self):
        self.handler.run()
        expected_source = self.test_assets('sherlock-and-queries.md')
        actual_source = os.path.join(self._temp_dir, 'sherlock-and-queries.md')
        with open(expected_source) as expected_source, open(
                actual_source) as actual_source:
            expected = expected_source.read()
            actual = actual_source.read()
            test.assert_equals(expected, actual, self.diff(actual, expected))

    def test_run_creates_readme(self):
        test_source = self.test_assets('sherlock-and-queries.md')
        with open(test_source) as test_source:
            self.handler._source = test_source.read()
        self.handler.run()
        expected_readme = self.test_assets('README.md')
        actual_readme = os.path.join(self._temp_dir, 'README.md')

        with open(expected_readme) as expected_readme, open(
                actual_readme) as actual_readme:
            expected = expected_readme.read()
            actual = actual_readme.read()
            test.assert_equals(expected, actual, self.diff(actual, expected))

    @staticmethod
    def diff(actual, expected):
        actual, expected = actual.splitlines(), expected.splitlines()
        summary = '\n'.join(difflib.unified_diff(expected, actual))
        full = '\n'.join(difflib.Differ().compare(expected, actual))
        return '\n{}\n\n{}'.format(summary, full)


if __name__ == '__main__':
    unittest.main()
