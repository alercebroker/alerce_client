import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_features_ztf_legacy(client):
    result = client.query_features(ZTF_OID)
    print("Legacy ZTF features:", result)
    assert result is not None


def test_query_features_lsst_multisurvey_not_implemented(client):
    with pytest.raises(NotImplementedError):
        client.query_features(LSST_OID, use_multisurvey_api=True, survey="lsst")


def test_query_features_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_features(ZTF_OID, use_multisurvey_api=True, survey="ztf")


def test_query_features_multisurvey_no_survey(client):
    with pytest.raises(ValueError):
        client.query_features(ZTF_OID, use_multisurvey_api=True)
