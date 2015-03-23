# coding=utf-8
import json
import os
import shutil

import pytest

from hackerranksetup.repository import Repository


sample_url = ('https://www.hackerrank.com/'
              'challenges/sherlock-and-queries')
tests_directory = os.path.dirname(__file__)
sample_assets = lambda x: os.path.join(tests_directory, 'test_assets', x)
sample_config = sample_assets('repository_config.json')


@pytest.fixture
def repo(monkeypatch, tmpdir):
    mock_config = tmpdir.join('repository_config.json').strpath
    shutil.copyfile(sample_config, mock_config)
    monkeypatch.setattr('hackerranksetup.repository.Repository.CONFIG_FILE',
                        mock_config)

    repository = Repository()
    assert repository.CONFIG_FILE == tmpdir.join('repository_config.json')
    return repository


def test_config_file_patched_properly(repo, tmpdir):
    assert repo.CONFIG_FILE == tmpdir.join('repository_config.json').strpath
    assert repo['Directory']['root'] == '/home/manu/code/HackerRankSetup/tests'


def test_getitem_magic(repo):
    actual = (
        repo['Archive']['Algorithms']['Warmup']['Solve me first']['path'])
    assert actual == 'algorithms/warmup/solve-me-first'

    assert repo['Current']['url'] == ('https://www.hackerrank.com/'
                                      'challenges/sherlock-and-queries')

    assert repo['Directory']['assets'] == ("/home/manu/code/"
                                           "HackerRankSetup/tests/assets")


def test_repo_converts_to_dict(repo):
    with open(sample_config) as f:
        assert dict(repo) == json.load(f)


def test_repo_saves_on_setitem(repo, tmpdir):
    repo['test'] = 'Success?'

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict['test'] == 'Success?'


# @pytest.mark.xfail(raises=KeyError)
def test_repo_saves_on_nested_setitem(repo, tmpdir):
    repo['test']['saves']['file'] = 'Success?'

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict['test']['saves']['file'] == 'Success?'


def test_repo_saves_on_delitem(repo, tmpdir):
    del repo['Current']

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict.get('Current') is None
    with pytest.raises(KeyError):
        assert tmp_repo_dict['Current']


@pytest.mark.xfail(raises=AssertionError)
def test_repo_saves_on_nested_delitem(repo, tmpdir):
    del repo['Current']['model']

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict['Current'].get('model') is None
    with pytest.raises(KeyError):
        assert tmp_repo_dict['Current']['model']


def test_repo_length(repo):
    assert len(repo) == 3
    assert len(repo) == len(repo.data)


def test_repo_iter(repo):
    assert list(repo) == ['Current', 'Directory', 'Archive']


def test_get_current_challenge(repo):
    assert repo.current_challenge == repo['Current']


def test_set_current_challenge(repo):
    del repo['Current']
    challenge_dict = dict(url=1, path=2, model=3)
    mock_challenge = type('mock_challenge', (object,), challenge_dict)

    repo.current_challenge = mock_challenge

    assert repo['Current']['url'] == challenge_dict['url']
    assert repo['Current']['path'] == challenge_dict['path']
    assert repo['Current']['model'] == challenge_dict['model']


# @pytest.mark.xfail(raises=KeyError)
def test_saves_on_set_current_challenge(repo, tmpdir):
    del repo['Current']
    challenge_dict = dict(url=1, path=2, model=3)
    mock_challenge = type('mock_challenge', (object,), challenge_dict)

    repo.current_challenge = mock_challenge

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict['Current']['url'] == challenge_dict['url']
    assert tmp_repo_dict['Current']['path'] == challenge_dict['path']
    assert tmp_repo_dict['Current']['model'] == challenge_dict['model']


def test_repo_saves_on_del_current_challenge(repo, tmpdir):
    del repo.current_challenge

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict.get('Current') is None
    with pytest.raises(KeyError):
        assert tmp_repo_dict['Current']


@pytest.mark.skipif
def test_archive_challege_adds_challenge_to_config(repo):
    pass


@pytest.mark.skipif
def test_archive_challege_saves_changes(repo):
    pass

