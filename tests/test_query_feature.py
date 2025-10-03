import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990
NAME = "feature_name"


def test_query_feature_ztf_legacy(client):
    result = client.query_feature(ZTF_OID, NAME)
    print("Legacy ZTF feature:", result)
    assert result is not None


def test_query_feature_lsst_multisurvey_not_implemented(client):
    with pytest.raises(NotImplementedError):
        client.query_feature(LSST_OID, NAME, use_multisurvey_api=True, survey="lsst")


def test_query_feature_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_feature(ZTF_OID, NAME, use_multisurvey_api=True, survey="ztf")


def test_query_feature_multisurvey_no_survey(client):
    with pytest.raises(ValueError):
        client.query_feature(ZTF_OID, NAME, use_multisurvey_api=True)
