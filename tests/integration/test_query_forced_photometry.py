import pytest
from alerce.core import Alerce
from alerce.exceptions import ObjectNotFoundError


@pytest.fixture
def client():
    return Alerce()


ZTF_OID = "ZTF18abeqwzl"
# Verified on api-lsst.alerce.online and Fink/LSST (2026-11-05).
LSST_OID = 313721466436714578
# Not in the database: a single missing OID returns 404, a list returns empty.
LSST_MISSING_OID = 169298433191444990


def test_query_forced_photometry_ztf_legacy(client):
    with pytest.warns(DeprecationWarning):
        result = client.query_forced_photometry(ZTF_OID)
    print("Legacy ZTF forced photometry:", result)
    assert result is not None


def test_query_forced_photometry_lsst(client):
    result = client.query_forced_photometry(LSST_OID, survey="lsst")
    assert len(result) > 0
    assert {d["oid"] for d in result} == {LSST_OID}


def test_query_forced_photometry_lsst_missing_oid(client):
    with pytest.raises(ObjectNotFoundError):
        client.query_forced_photometry(LSST_MISSING_OID, survey="lsst")


def test_query_forced_photometry_lsst_missing_oid_list(client):
    result = client.query_forced_photometry(
        [LSST_MISSING_OID, LSST_MISSING_OID + 1], survey="lsst"
    )
    assert result == []


def test_query_forced_photometry_invalid_survey(client):
    with pytest.raises(ValueError):
        client.query_forced_photometry(ZTF_OID, survey="invalid")
