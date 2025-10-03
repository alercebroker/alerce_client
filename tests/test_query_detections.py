import pytest
from alerce.core import Alerce

# Dummy OIDs for testing
ZTF_OID = "ZTF20aaelulu"
LSST_OID = 169298433191444990


@pytest.fixture
def client():
    return Alerce()


def test_query_detections_ztf_legacy(client):
    # Should succeed for legacy ZTF client
    result = client.query_detections(ZTF_OID)
    print("Legacy ZTF detections:", result)
    assert result is not None


def test_query_detections_lsst_multisurvey(client):
    # Should succeed for LSST in multisurvey
    result = client.query_detections(LSST_OID, use_multisurvey_api=True, survey="lsst")
    print("Multisurvey LSST detections:", result)
    assert result is not None


def test_query_detections_ztf_multisurvey_fails(client):
    # Should raise NotImplementedError for ZTF in multisurvey
    with pytest.raises(NotImplementedError):
        client.query_detections(ZTF_OID, use_multisurvey_api=True, survey="ztf")


def test_query_detections_multisurvey_no_survey(client):
    # Should raise ValueError if survey is not provided
    with pytest.raises(ValueError):
        client.query_detections(ZTF_OID, use_multisurvey_api=True)
