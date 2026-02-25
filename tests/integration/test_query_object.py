import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 313765480543813793


def test_query_object_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_object(ZTF_OID)
    print("Legacy ZTF object:", result)
    assert result is not None


def test_query_object_lsst(client):
    result = client.query_object(LSST_OID, survey="lsst")
    print("Multisurvey LSST object:", result)
    assert result is not None


def test_query_object_lsst_with_extra(client):
    result = client.query_object(LSST_OID, survey="lsst", return_survey_extra=True)
    print("Multisurvey LSST object with extra:", result)
    assert result is not None


def test_query_object_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_object(ZTF_OID, survey="invalid")
