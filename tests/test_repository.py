# coding=utf-8
import json
import shutil

import pytest

from hackerranksetup import Repository
from tests import sample_config


@pytest.fixture
def repo(monkeypatch, tmpdir):
    mock_config = tmpdir.join('repository_config.json').strpath
    shutil.copyfile(sample_config, mock_config)
    # monkeypatch.setattr('hackerranksetup.Repository.CONFIG_FILE',
    #                     mock_config)

    repository = Repository(mock_config)
    # assert repository.CONFIG_FILE == tmpdir.join('repository_config.json')
    return repository


def test_config_file_patched_properly(repo, tmpdir):
    assert repo.config_file == tmpdir.join('repository_config.json').strpath
    assert repo.root == '/home/manu/code/HackerRankSetup/tests'


def test_getitem_magic(repo):
    actual = (repo.archive['Algorithms']['Warmup']['Solve me first']['path'])
    assert actual == 'algorithms/warmup/solve-me-first'

    assert repo.current_challenge['url'] == ('https://www.hackerrank.com/'
                                             'challenges/sherlock-and-queries')

    assert repo.assets == ("/home/manu/code/"
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
def test_archive_challenge_adds_challenge_to_config(repo):
    pass


@pytest.mark.skipif
def test_archive_challenge_saves_changes(repo):
    pass

