# coding=utf-8
import json
import cPickle

import pytest

from hackerranksetup import Challenge
from tests import sample_url, sample_assets


with open(sample_assets('challenge_request.p')) as response:
    challenge_request = cPickle.load(response)


@pytest.fixture
def challenge(monkeypatch):
    monkeypatch.setattr('requests.get',
                        lambda _: challenge_request)
    challenge_ = Challenge(sample_url)

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