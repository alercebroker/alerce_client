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
    params = {"firstmjd": [60000, 60100], "ndet": [5, 10]}
    result = client.query_objects(
        format="pandas", index="oid", sort="firstmjd", **params
    )
    print("Legacy ZTF objects:", result)
    assert result is not None


def test_query_objects_lsst_multisurvey_1(client):
    params = {"firstmjd": [60000, 61000], "n_det": [5, 10]}
    result = client.query_objects(use_multisurvey_api=True, survey="lsst", **params)
    print("Multisurvey LSST objects:", result)
    assert result is not None


def test_query_objects_lsst_multisurvey_2(client):
    params = {"classifier": "rubin_stamp_1", "class_name": "SN"}
    result = client.query_objects(use_multisurvey_api=True, survey="lsst", **params)
    print("Multisurvey LSST objects:", result)
    assert result is not None


def test_query_objects_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_objects(use_multisurvey_api=True, survey="ztf")
