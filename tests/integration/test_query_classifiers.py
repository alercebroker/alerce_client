import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


OID = "ZTF20aaelulu"


def test_query_classifiers_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_classifiers()
    print("Legacy ZTF classifiers:", result)
    assert result is not None


def test_query_classifiers_lsst(client):
    result = client.query_classifiers(survey="lsst")
    assert isinstance(result, list)
    assert len(result) > 0
    assert "classifier_name" in result[0]


def test_query_classifiers_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_classifiers(survey="invalid")
