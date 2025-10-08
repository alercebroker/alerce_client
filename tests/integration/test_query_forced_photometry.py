import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_forced_photometry_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_forced_photometry(ZTF_OID)
    print("Legacy ZTF forced photometry:", result)
    assert result is not None


def test_query_forced_photometry_lsst(client):
    result = client.query_forced_photometry(LSST_OID, survey="lsst")
    print("Multisurvey LSST forced photometry:", result)
    assert result is not None


def test_query_forced_photometry_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_forced_photometry(ZTF_OID, survey="invalid")
