import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 171141215992414254
LSST_FEATURE_NAME = "Coordinate_x"
NAME = "feature_name"


def test_query_feature_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_feature(ZTF_OID, NAME)
    print("Legacy ZTF feature:", result)
    assert result is not None


def test_query_feature_lsst(client):
    result = client.query_feature(LSST_OID, LSST_FEATURE_NAME, survey="lsst")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["name"] == LSST_FEATURE_NAME


def test_query_feature_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_feature(ZTF_OID, NAME, survey="invalid")
