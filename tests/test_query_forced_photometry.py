import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_forced_photometry_ztf_legacy(client):
    result = client.query_forced_photometry(ZTF_OID)
    print("Legacy ZTF forced photometry:", result)
    assert result is not None


def test_query_forced_photometry_lsst_multisurvey(client):
    result = client.query_forced_photometry(
        LSST_OID, use_multisurvey_api=True, survey="lsst"
    )
    print("Multisurvey LSST forced photometry:", result)
    assert result is not None


def test_query_forced_photometry_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_forced_photometry(ZTF_OID, use_multisurvey_api=True, survey="ztf")


def test_query_forced_photometry_multisurvey_no_survey(client):
    with pytest.raises(ValueError):
        client.query_forced_photometry(LSST_OID, use_multisurvey_api=True)
