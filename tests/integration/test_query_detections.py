import pytest
from alerce.core import Alerce

# Dummy OIDs for testing
ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


@pytest.fixture
def client():
    return Alerce()


def test_query_detections_ztf_legacy_signature(client):
    # Test the legacy signature without survey parameter
    # It should default to ZTF but raise a deprecation warning
    with pytest.warns(DeprecationWarning):
        result = client.query_detections(ZTF_OID)
    print("ZTF detections:", result)
    assert result is not None


def test_query_detections_ztf(client):
    result = client.query_detections(ZTF_OID, survey="ztf")
    print("ZTF detections:", result)
    assert result is not None


def test_query_detections_lsst(client):
    result = client.query_detections(LSST_OID, survey="lsst")
    print("Multisurvey LSST detections:", result)
    assert result is not None


def test_query_detections_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_detections(ZTF_OID, survey="invalid_survey")
