import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990
NAME = "feature_name"


def test_query_feature_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_feature(ZTF_OID, NAME)
    print("Legacy ZTF feature:", result)
    assert result is not None


def test_query_feature_lsst(client):
    with pytest.raises(NotImplementedError):
        client.query_feature(LSST_OID, NAME, survey="lsst")


def test_query_feature_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_feature(ZTF_OID, NAME, survey="invalid")
