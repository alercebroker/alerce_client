import pandas as pd
import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 313765480543813793


def test_query_objects_ztf_legacy(client):
    params = {"firstmjd": [60000, 60100], "ndet": [5, 10]}
    result = client.query_objects(
        format="pandas", index="oid", sort="firstmjd", survey="ztf", **params
    )
    print("Legacy ZTF objects:", result)
    assert result is not None


def test_query_objects_ztf_legacy_signature(client):
    params = {"firstmjd": [60000, 60100], "ndet": [5, 10]}
    with pytest.warns(DeprecationWarning):
        result = client.query_objects(
            format="pandas", index="oid", sort="firstmjd", **params
        )
    print("Legacy ZTF objects (legacy signature):", result)
    assert result is not None


def test_query_objects_lsst_multisurvey_1(client):
    params = {"classifier": "stamp_classifier_rubin", "class_name": "SN"}
    result = client.query_objects(survey="lsst", format="json", **params)
    for item in result:
        assert item["class_name"] == "SN"
    print("Multisurvey LSST objects:", result)
    assert result is not None


def test_query_objects_lsst_multisurvey_classifier_without_class_name(client):
    params = {"classifier": "stamp_classifier_rubin", "n_det": [5, 10]}
    result = client.query_objects(survey="lsst", format="json", **params)
    result_items_df = pd.DataFrame(result)
    print("Multisurvey LSST objects:")
    print(result_items_df)
    assert result is not None


def test_query_objects_lsst_multisurvey_no_classifier(client):
    params = {
        "firstmjd": [60000, 61000],
        "n_det": [5, 10],
        "ranking": 1,
        "page_size": 20,
        "page": 1,
        "order_by": "probability",
        "order_mode": "DESC",
    }
    result = client.query_objects(
        index="oid", sort="firstmjd", survey="lsst", format="json", **params
    )
    print("Multisurvey LSST objects:", result)
    assert result is not None


def test_query_objects_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_objects(survey="invalid")
