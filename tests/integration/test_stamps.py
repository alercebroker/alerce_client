import numpy as np
import pytest
from astropy.io.fits import HDUList, PrimaryHDU


from alerce.core import Alerce


def test_plot_stamp():
    alerce = Alerce()
    with pytest.warns(RuntimeWarning):
        r = alerce.plot_stamps(oid="ZTF18abjpdlh", candid="570448435315010000")
        assert r is None


def test_get_stamp_ztf_without_candid():
    alerce = Alerce()
    r = alerce.get_stamps(oid="ZTF18abjpdlh")
    for hdu in r:
        assert isinstance(hdu.data, np.ndarray)


def test_get_stamp_ztf_with_candid():
    alerce = Alerce()
    r = alerce.get_stamps(oid="ZTF18abjpdlh", candid="570448435315010000")
    for hdu in r:
        assert isinstance(hdu.data, np.ndarray)


def test_get_stamp_lsst():
    alerce = Alerce()
    r = alerce.get_stamps(
        survey="lsst",
        oid=169298436520149069,
        measurement_id=169298436520149069,
        use_multisurvey_api=True,
    )
    assert isinstance(r, dict)
    for hdu in r.values():
        assert isinstance(hdu, PrimaryHDU)


def test_get_stamp_lsst_without_measurement_id():
    alerce = Alerce()
    r = alerce.get_stamps(
        survey="lsst",
        oid=169298436520149069,
        use_multisurvey_api=True,
    )
    assert isinstance(r, dict)
    for hdu in r.values():
        assert isinstance(hdu, PrimaryHDU)
