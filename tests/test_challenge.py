# coding=utf-8
import json

from mock import Mock
import pytest
import requests

from hackerranksetup import Challenge
from tests import sample_url, sample_assets


with open(sample_assets('challenge_request.json')) as response:
    challenge_request = json.load(response)


@pytest.fixture
def mock_requests():
    mock_request_ = Mock(spec=requests)
    mock_response = Mock()
    mock_response.json.return_value = challenge_request
    mock_request_.get.return_value = mock_response
    return mock_request_


@pytest.fixture
def challenge(mock_requests):
    challenge_ = Challenge(sample_url, requests=mock_requests)

    return challenge_


# noinspection PyProtectedMember
def test_challenge_initializes_properly(challenge):
    assert challenge.url == sample_url
    assert challenge._rest_endpoint is None
    assert challenge._model is None


def test_url_property_creates_url():
    challenge = Challenge('/sherlock-and-queries')
    assert challenge.url == sample_url


def test_loads_model_into_json(challenge):
    with open(sample_assets('challenge_request.json')) as response:
        expected = json.load(response)['model']
    assert challenge.model == expected


def test_calculates_rest_endpoint(challenge):
    expected_endpoint = ('https://www.hackerrank.com/'
                         'rest/contests/master/challenges/'
                         'sherlock-and-queries')
    assert challenge.rest_endpoint == expected_endpoint


def test_rest_endpoint_raises_validation_error(challenge):
    bad_url = 'asdfasdf'
    with pytest.raises(ValueError):
        challenge.url = bad_url


def test_destination_returns_relpath_for_challenge(challenge):
    expected = 'algorithms/summations-and-algebra/sherlock-and-queries'
    assert challenge.path == expected


def test_json(challenge):
    model = challenge.json()

    assert model == challenge.model
    assert model['url'] == sample_url


def test_from_repo(challenge, mock_requests):
    repo = challenge.json()
    Challenge.from_repo(repo, requests=mock_requests)