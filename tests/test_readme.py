# coding=utf-8
import json
import os.path

import mock
import pytest

from hackerranksetup.readme import Readme


tests_directory = os.path.dirname(__file__)
sample_assets = lambda x: os.path.join(tests_directory, 'test_assets', x)

@pytest.fixture
def readme(monkeypatch, tmpdir):
    challenge_url = ('https://www.hackerrank.com/'
                     'challenges/sherlock-and-queries')
    challenge_model = json.load(open(sample_assets('challenge_request.json')))[
        'model']
    challenge = mock.MagicMock(model=challenge_model, url=challenge_url)

    teximage_dict = json.load(open(sample_assets('readme_teximage.json')))

    monkeypatch.setattr('hackerranksetup.teximage.TexImage',
                        lambda _: teximage_dict)
    tmpdir_destination = tmpdir.mkdir('workspace')
    tmpdir_assets = tmpdir.mkdir('assets')
    readme_ = Readme(challenge, tmpdir_destination.strpath,
                     tmpdir_assets.strpath)

    assert readme_.challenge.model is challenge_model
    assert readme_.challenge.url is challenge_url
    return readme_


# noinspection PyProtectedMember
def test_readme_initializes_properly(readme, tmpdir):
    assert readme.challenge.model['name'] == 'Sherlock and Queries'
    assert readme.challenge.model['slug'] == 'sherlock-and-queries'
    assert readme.destination == tmpdir.join('workspace').strpath
    assert readme.assets == tmpdir.join('assets').strpath
    assert readme._source is None
    assert readme._readme is None


def test_compile_source_from_model(readme):
    with open(sample_assets('readme_source.md')) as f:
        expected_source = f.read()
    assert readme.source == expected_source


def test_compile_readme_from_source(readme):
    with open(sample_assets('readme_source.md')) as f:
        readme._source = f.read()

    with open(sample_assets('readme_readme.md')) as f:
        expected_readme = f.read()

    assert readme.readme == expected_readme


def test_saves_readme(readme, tmpdir):
    with open(sample_assets('readme_source.md')) as f:
        readme._source = f.read()
    with open(sample_assets('readme_readme.md')) as f:
        expected = f.read()

    readme.save()
    with open(tmpdir.join('workspace', 'README.md').strpath) as f:
        actual = f.read()

    assert actual == expected