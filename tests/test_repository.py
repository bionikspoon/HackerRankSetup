# coding=utf-8
import json
import shutil

from mock import Mock
import pytest

from hackerranksetup import Repository, Challenge
from tests import sample_config, sample_url, sample_assets


challenge_model = json.load(open(sample_assets('challenge_request.json')))[
    'model']


@pytest.fixture
def mock_challenge():
    mock = Mock(spec=Challenge)
    mock.json.return_value = {'test': 'success'}
    mock.from_repo.return_value = Challenge(sample_url, model=challenge_model,
                                            requests=Mock())
    return mock


@pytest.fixture
def repo(tmpdir, mock_challenge):
    mock_config = tmpdir.join('repository_config.json').strpath
    shutil.copyfile(sample_config, mock_config)

    repository = Repository(mock_config, mock_challenge)
    return repository


def test_config_file_patched_properly(repo, tmpdir):
    assert repo.config_file == tmpdir.join('repository_config.json').strpath
    assert repo.root == '/home/manu/code/HackerRankSetup/tests'


def test_root(repo):
    assert repo.root == '/home/manu/code/HackerRankSetup/tests'


def test_assets(repo):
    assert repo.assets == '/home/manu/code/HackerRankSetup/tests/assets'


def test_workspace(repo):
    assert repo.workspace == '/home/manu/code/HackerRankSetup/tests/workspace'


def test_get_current_challenge(repo):
    assert repo.current_challenge == json.load(open(sample_config))['Current']


def test_set_current_challenge(repo, mock_challenge):
    del repo.current_challenge
    assert repo.current_challenge is None

    repo.current_challenge = mock_challenge

    assert repo.current_challenge['test'] == 'success'


def test_delete_current_config(repo):
    del repo.current_challenge
    assert repo.current_challenge is None


def test_saves_on_set_current_challenge(repo, mock_challenge, tmpdir):
    del repo.current_challenge
    assert repo.current_challenge is None

    repo.current_challenge = mock_challenge

    assert repo.current_challenge['test'] == 'success'

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict['Current']['test'] == 'success'


def test_saves_on_del_current_challenge(repo, tmpdir):
    del repo.current_challenge
    assert repo.current_challenge is None

    with tmpdir.join('repository_config.json').open() as f:
        tmp_repo_dict = json.load(f)

    assert tmp_repo_dict.get('Current') is None
    with pytest.raises(KeyError):
        assert tmp_repo_dict['Current']


def test_nested_archive(repo):
    repo.data = {}
    # assert repo.archive is None
    # assert repo.current_challenge is None

    mock = Mock()
    mock.track_main = "test track main"
    mock.track_sub = "test track sub"
    mock.name = "test name"
    mock.url = " test url"
    mock.path = "test path"
    mock.json.return_value = {'test': 'success'}

    repo.data['Current'] = mock
    repo.Challenge.from_repo.return_value = mock
    del repo.current_challenge

    expected_partial = {'path': 'test path', 'url': ' test url'}
    expected = {
        'test track main': {'test track sub': {'test name': expected_partial}}}
    assert repo.data['Archive'] == expected


def test_archive(repo):
    expected = {'test': 'success'}
    repo.data['Archive'] = expected
    assert repo.archive == expected
