# coding=utf-8
import json

import mock
import pytest

from hackerranksetup import Readme
from tests import sample_assets


@pytest.fixture
def readme(monkeypatch, tmpdir):
    challenge_url = ('https://www.hackerrank.com/'
                     'challenges/sherlock-and-queries')
    challenge_model = json.load(open(sample_assets('challenge_request.json')))[
        'model']
    challenge = mock.MagicMock(model=challenge_model, url=challenge_url)

    teximage_dict = json.load(open(sample_assets('readme_teximage.json')))

    monkeypatch.setattr('hackerranksetup.TexImage',
                        lambda _: teximage_dict)
    tmpdir_destination = tmpdir.mkdir('workspace')
    tmpdir_assets = tmpdir.mkdir('assets')
    readme_ = Readme(challenge, tmpdir_destination.strpath,
                     tmpdir_assets.strpath)

    assert readme_.challenge.model is challenge_model
    assert readme_.challenge.url is challenge_url
    return readme_


@pytest.fixture
def readme_unicode(readme):
    # TODO
    # with open(sample_assets('readme_challenge_unicode.p')) as f:
    # readme.challenge = cPickle.load(f)
    return readme


def test_readme_initializes_name(readme):
    assert readme.challenge.name == 'Sherlock and Queries'


def test_readme_initializes_slug(readme):
    assert readme.challenge.slug == 'sherlock-and-queries'


def test_readme_initializes_destination(readme, tmpdir):
    assert readme.destination == tmpdir.join('workspace').strpath


def test_readme_initializes_assets(readme, tmpdir):
    assert readme.assets == tmpdir.join('assets').strpath


def test_readme_initializes_source(readme):
    # noinspection PyProtectedMember
    assert readme._source is None


def test_readme_initializes_readme(readme):
    # noinspection PyProtectedMember
    assert readme._readme is None


def test_compile_source_from_model(readme):
    with open(sample_assets('readme_source.md')) as f:
        expected_source = f.read()
    assert readme.source == expected_source

@pytest.mark.skipif
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


def test_source_can_work_with_unicode(readme_unicode):
    # TODO test unicode
    with open(sample_assets('readme_source_unicode.md')) as f:
        expected = f.read()
        # assert readme_unicode.source == expected


def test_escapes_literal_parens(readme):
    # TODO
    pass