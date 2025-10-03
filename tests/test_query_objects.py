import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_objects_multisurvey_no_survey(client):
    with pytest.raises(ValueError):
        client.query_objects(use_multisurvey_api=True)


def test_query_objects_ztf_legacy(client):
    result = client.query_objects()
    print("Legacy ZTF objects:", result)
    assert result is not None


def test_query_objects_lsst_multisurvey(client):
    result = client.query_objects(use_multisurvey_api=True, survey="lsst")
    print("Multisurvey LSST objects:", result)
    assert result is not None


def test_query_objects_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_objects(use_multisurvey_api=True, survey="ztf")
