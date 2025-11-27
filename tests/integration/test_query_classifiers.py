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
    with pytest.raises(NotImplementedError):
        client.query_classifiers(survey="lsst")


def test_query_classifiers_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_classifiers(survey="invalid")
