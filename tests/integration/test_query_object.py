import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_object_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_object(ZTF_OID)
    print("Legacy ZTF object:", result)
    assert result is not None


def test_query_object_lsst(client):
    result = client.query_object(LSST_OID, survey="lsst")
    print("Multisurvey LSST object:", result)
    assert result is not None


def test_query_object_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_object(ZTF_OID, survey="invalid")
