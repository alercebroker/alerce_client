import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


CLASSIFIER_NAME = "lc_classifier"
CLASSIFIER_VERSION = "hierarchical_random_forest_1.0.0"


def test_query_classes_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_classes(CLASSIFIER_NAME, CLASSIFIER_VERSION)
    print("Legacy ZTF classes:", result)
    assert result is not None


def test_query_classes_lsst(client):
    with pytest.raises(NotImplementedError):
        client.query_classes(CLASSIFIER_NAME, CLASSIFIER_VERSION, survey="lsst")


def test_query_classes_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_classes(CLASSIFIER_NAME, CLASSIFIER_VERSION, survey="invalid")
