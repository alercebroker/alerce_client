import pytest
from alerce.core import Alerce


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
LSST_OID = 171141215992414254


def test_query_magstats_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_magstats(ZTF_OID)
    print("Legacy ZTF magstats:", result)
    assert result is not None


def test_query_magstats_lsst(client):
    result = client.query_magstats(LSST_OID, survey="lsst")
    assert isinstance(result, list)
    assert len(result) > 0


def test_query_magstats_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_magstats(ZTF_OID, survey="invalid")
