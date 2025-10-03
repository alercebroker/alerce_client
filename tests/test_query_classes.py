import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


CLASSIFIER_NAME = "lc_classifier"
CLASSIFIER_VERSION = "hierarchical_random_forest_1.0.0"


def test_query_classes_ztf_legacy(client):
    result = client.query_classes(CLASSIFIER_NAME, CLASSIFIER_VERSION)
    print("Legacy ZTF classes:", result)
    assert result is not None


def test_query_classes_lsst_multisurvey_not_implemented(client):
    with pytest.raises(NotImplementedError):
        client.query_classes(
            CLASSIFIER_NAME, CLASSIFIER_VERSION, use_multisurvey_api=True, survey="lsst"
        )


def test_query_classes_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_classes(
            CLASSIFIER_NAME, CLASSIFIER_VERSION, use_multisurvey_api=True, survey="ztf"
        )


def test_query_classes_multisurvey_no_survey(client):
    with pytest.raises(ValueError):
        client.query_classes(
            CLASSIFIER_NAME, CLASSIFIER_VERSION, use_multisurvey_api=True
        )
