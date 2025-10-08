import pytest
from unittest.mock import patch
import numpy as np
from astropy.io.fits import HDUList, PrimaryHDU
from urllib.error import HTTPError
import sys
import os

sys.path.append("..")
from alerce.core import Alerce


FILE_PATH = os.path.dirname(__file__)
EXAMPLE_PATH = os.path.join(FILE_PATH, "examples/example.fits.gz")


class Dummy:
    def __init__(self, content):
        self.content = content


with open(EXAMPLE_PATH, "rb") as f:
    EXAMPLE_FITS = Dummy(f.read())


def test_plot_stamp():
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        r = alerce.plot_stamps(oid="ZTF18abjpdlh", candid="570448435315010000")
        assert r is None


@pytest.mark.filterwarnings("ignore:Keyword name")
@patch("requests.Session.request", return_value=EXAMPLE_FITS)
def test_get_stamp_fits(mock_fits):
    alerce = Alerce()
    r = alerce.get_stamps(oid="ZTF18abjpdlh", candid="570448435315010000")
    assert isinstance(r, HDUList)


@pytest.mark.filterwarnings("ignore:Keyword name")
@patch("requests.Session.request", return_value=EXAMPLE_FITS)
def test_get_stamp_numpy(mock_fits):
    alerce = Alerce()
    r = alerce.get_stamps(
        oid="ZTF18abjpdlh", candid="570448435315010000", format="numpy"
    )
    assert len(r) == 3
    for i in r:
        assert isinstance(i, np.ndarray)


@patch(
    "alerce.stamps.fits_open",
    side_effect=HTTPError(url="mock://test", code=500, msg="mock", hdrs={}, fp=None),
)
def test_exception_stamp(mock_fits):
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        r = alerce.plot_stamps(oid="ZTF18abjpdlh", candid="570448435315010001")
        assert r is None


@patch("requests.Session.request", return_value=EXAMPLE_FITS)
def test_get_stamp_invalid_oid(mock_fits):
    alerce = Alerce()
    # Simulate an invalid OID by patching the response to empty content
    with patch("alerce.stamps.fits_open", side_effect=OSError("No FITS data")):
        with pytest.raises(OSError):
            alerce.get_stamps(oid="INVALID_OID", candid="570448435315010000")


@patch("requests.Session.request", return_value=EXAMPLE_FITS)
def test_get_avro_valid_oid(mock_fits):
    alerce = Alerce()
    with patch("alerce.stamps.open", return_value=EXAMPLE_FITS):
        result = alerce.get_avro(oid="ZTF18abjpdlh", candid="570448435315010000")
        assert isinstance(result, bytes) or result is not None


@patch(
    "requests.Session.request",
    side_effect=HTTPError(url="mock://test", code=404, msg="mock", hdrs={}, fp=None),
)
def test_get_avro_invalid_oid(mock_fits):
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        result = alerce.get_avro(oid="INVALID_OID", candid="570448435315010000")
        assert result is None


def test_multisurvey_not_implemented():
    alerce = Alerce()
    with pytest.raises(NotImplementedError):
        alerce.get_stamps(
            oid="ZTF18abjpdlh",
            candid="570448435315010000",
            use_multisurvey_api=True,
            survey="lsst",
        )
    with pytest.raises(NotImplementedError):
        alerce.plot_stamps(
            oid="ZTF18abjpdlh",
            candid="570448435315010000",
            use_multisurvey_api=True,
            survey="lsst",
        )
    with pytest.raises(NotImplementedError):
        alerce.get_avro(
            oid="ZTF18abjpdlh",
            candid="570448435315010000",
            use_multisurvey_api=True,
            survey="lsst",
        )
