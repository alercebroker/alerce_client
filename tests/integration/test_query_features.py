import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_features_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_features(ZTF_OID)
    print("Legacy ZTF features:", result)
    assert result is not None


def test_query_features_lsst(client):
    with pytest.raises(NotImplementedError):
        client.query_features(LSST_OID, survey="lsst")


def test_query_features_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_features(ZTF_OID, survey="invalid")
