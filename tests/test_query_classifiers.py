import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


OID = "ZTF20aaelulu"


def test_query_classifiers_ztf_legacy(client):
    result = client.query_classifiers()
    print("Legacy ZTF classifiers:", result)
    assert result is not None


def test_query_classifiers_lsst_multisurvey_not_implemented(client):
    with pytest.raises(NotImplementedError):
        client.query_classifiers(use_multisurvey_api=True, survey="lsst")


def test_query_classifiers_ztf_multisurvey_fails(client):
    with pytest.raises(NotImplementedError):
        client.query_classifiers(use_multisurvey_api=True, survey="ztf")


def test_query_classifiers_multisurvey_no_survey(client):
    with pytest.raises(ValueError):
        client.query_classifiers(use_multisurvey_api=True)
