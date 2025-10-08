import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 169298433191444990


def test_query_probabilities_ztf_legacy(client):
    # TODO: API currently has a bug that prevents this from working.
    # "classifier" field should be optional, but it is not.
    with pytest.warns(DeprecationWarning):
        result = client.query_probabilities(ZTF_OID)
    print("Legacy ZTF probabilities:", result)
    assert result is not None


def test_query_probabilities_ztf_legacy_with_classifier(client):
    result = client.query_probabilities(ZTF_OID, classifier="lc_classifier")
    print("Legacy ZTF probabilities with classifier:", result)
    assert result is not None


def test_query_probabilities_lsst(client):
    result = client.query_probabilities(LSST_OID, survey="lsst")
    print("Multisurvey LSST probabilities:", result)
    assert result is not None


def test_query_probabilities_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_probabilities(ZTF_OID, survey="invalid")
