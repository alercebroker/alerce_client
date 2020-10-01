import pytest
from unittest.mock import patch
from astropy.io.fits import HDUList
from urllib.error import HTTPError
import astropy.io.fits as fio
import sys
import os

from alerce.exceptions import ObjectNotFoundError

sys.path.append("..")
from alerce.core import Alerce

FILE_PATH = os.path.dirname(__file__)
EXAMPLE_PATH = os.path.join(FILE_PATH, "examples/example.fits")
EXAMPLE_FITS = fio.open(EXAMPLE_PATH)


def test_plot_stamp():
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        r = alerce.plot_stamp(oid="ZTF18abjpdlh", candid="570448435315010000")
        assert r is None


def test_plot_stamp_without_candid():
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        r = alerce.plot_stamp(oid="ZTF18abjpdlh")
        assert r is None


@patch('alerce.stamps.fits_open', return_value=EXAMPLE_FITS)
def test_get_stamp(mock_fits):
    alerce = Alerce()
    r = alerce.get_stamps(oid="ZTF18abjpdlh", candid="570448435315010000")
    assert isinstance(r, HDUList)


@patch('alerce.stamps.fits_open', return_value=EXAMPLE_FITS)
def test_get_stamp_without_candid(mock_fits):
    alerce = Alerce()
    r = alerce.get_stamps(oid="ZTF18abjpdlh")
    assert isinstance(r, HDUList)


@patch('alerce.stamps.fits_open', return_value=EXAMPLE_FITS)
def test_get_nonexistent_stamp(mock_fits):
    alerce = Alerce()
    with pytest.raises(ObjectNotFoundError):
        alerce.get_stamps(oid="testo")


@patch('alerce.stamps.fits_open', side_effect=HTTPError(url="mock://test", code=500, msg="mock", hdrs={}, fp=None))
def test_exception_stamp(mock_fits):
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        r = alerce.plot_stamp(oid="ZTF18abjpdlh", candid="570448435315010001")
        assert r is None


def test_init_alerce_path():
    alerce = Alerce().load_config_from_file("testo")
    assert alerce is None


def test_init_alerce_object():
    alerce = Alerce().load_config_from_object({})
    assert alerce is None
