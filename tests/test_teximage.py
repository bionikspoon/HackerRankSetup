# coding=utf-8
import hashlib
import cPickle

import pytest

from hackerranksetup import TexImage
from tests import sample_assets


@pytest.fixture
def teximage(monkeypatch, tmpdir):
    def mock_requests_get(_, params=None):
        code = params['chl']
        hash_id = hashlib.md5(code).hexdigest()
        file_name = '{}_{}.{}'.format('teximage', hash_id, 'p')

        return cPickle.load(open(sample_assets(file_name)))

    monkeypatch.setattr('requests.get',
                        mock_requests_get)
    teximage_ = TexImage(tmpdir.mkdir('assets').strpath)

    return teximage_


@pytest.fixture
def sample_data():
    sample_tex_formulas = (
        '$1 \\le A[i], C[i] \\le 10^5$', '$1 \\le B[i] \\le N$', '$(10^9 + 7)$')
    sample_image_names = ('d133006232caf463e513a0ef1f36103c.png',
                          'ef9ba375db3112e1c88aa798dd3522c4.png',
                          'c4e61dbf8b36a31aa53c4e418152f3d2.png')
    data_ = {'codes': sample_tex_formulas, 'names': sample_image_names}
    return data_


def test_teximage_initializes_properly(teximage, tmpdir):
    teximage.assets = tmpdir.join('assets').strpath


def test_returns_hashed_filename(teximage, sample_data):
    for actual, expected in zip(sample_data['codes'], sample_data['names']):
        assert teximage.get(actual) == expected


def test_saves_image_to_png(teximage, tmpdir, sample_data):
    map(teximage.get, sample_data['codes'])

    for sample_name in sample_data['names']:
        with open(tmpdir.join('assets', sample_name).strpath) as f:
            actual = f.read()
        with open(sample_assets('{}_{}'.format('teximage', sample_name))) as f:
            expected = f.read()

        assert actual == expected