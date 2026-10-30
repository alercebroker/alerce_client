import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


CLASSIFIER_NAME = "lc_classifier"
CLASSIFIER_VERSION = "hierarchical_random_forest_1.0.0"

LSST_CLASSIFIER_NAME = "stamp_classifier_rubin_beta"
LSST_CLASSIFIER_VERSION = "2.0.1"


def test_query_classes_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_classes(CLASSIFIER_NAME, CLASSIFIER_VERSION)
    print("Legacy ZTF classes:", result)
    assert result is not None


def test_query_classes_lsst(client):
    result = client.query_classes(
        LSST_CLASSIFIER_NAME, LSST_CLASSIFIER_VERSION, survey="lsst"
    )
    assert isinstance(result, list)
    assert len(result) > 0
    assert "name" in result[0]


def test_query_classes_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_classes(CLASSIFIER_NAME, CLASSIFIER_VERSION, survey="invalid")
