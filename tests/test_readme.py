# coding=utf-8
import json
from mock import Mock

import pytest
import requests

from hackerranksetup import Readme, Challenge, TexImage
from tests import sample_assets, sample_url

teximage_dict = json.load(open(sample_assets('readme_teximage.json')))


@pytest.fixture
def mock_tex_image():
    mock = Mock(spec=TexImage)
    mock.return_value = mock
    mock.get.side_effect = teximage_dict.get
    return mock


@pytest.fixture
def mock_challenge():
    challenge_model = json.load(open(sample_assets('challenge_request.json')))[
        'model']
    mock_challenge_ = Challenge(sample_url, model=challenge_model,
                                requests=Mock(spec=requests))
    return mock_challenge_


@pytest.fixture
def readme(tmpdir, mock_tex_image, mock_challenge):
    tmpdir_destination = tmpdir.mkdir('workspace')
    tmpdir_assets = tmpdir.mkdir('assets')
    readme_ = Readme(mock_challenge, tmpdir_destination.strpath,
                     tmpdir_assets.strpath, tex_image=mock_tex_image)

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


def test_compile_readme_from_source(readme):
    with open(sample_assets('readme_source.md')) as f:
        readme._source = f.read()

    with open(sample_assets('readme_readme.md')) as f:
        expected_readme = f.read()

    assert readme.readme == expected_readme


def test_saves_readme(tmpdir, mock_challenge, mock_tex_image):
    with open(sample_assets('readme_source.md')) as f:
        readme._source = f.read()
    with open(sample_assets('readme_readme.md')) as f:
        expected = f.read()

    tmpdir_destination = tmpdir.mkdir('workspace')
    tmpdir_assets = tmpdir.mkdir('assets')
    Readme.save(mock_challenge, tmpdir_destination.strpath,
                tmpdir_assets.strpath, tex_image=mock_tex_image)

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