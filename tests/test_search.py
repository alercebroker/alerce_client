from unittest.mock import patch
from requests import Session
from pandas import DataFrame
from astropy.table import Table
import sys
import pytest

sys.path.append("..")
from alerce.core import Alerce
from alerce.exceptions import ObjectNotFoundError, FormatValidationError, ParseError

alerce = Alerce()


@patch.object(Session, "request")
def test_query_objects(mock_request):
    def mock_result():
        return {"items": [{"oid": "test"}]}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.query_objects(classifier="lc_classifier")
    assert r is not None


@patch.object(Session, "request")
def test_query_objects_not_found(mock_request):
    mock_request.return_value.status_code = 404
    with pytest.raises(ObjectNotFoundError):
        alerce.query_objects(classifier="lc_classifier")


@patch.object(Session, "request")
def test_query_objects_parser_error(mock_request):
    mock_request.return_value.status_code = 400
    with pytest.raises(ParseError):
        alerce.query_objects(classifier=123)


@patch.object(Session, "request")
def test_query_objects_format_error(mock_request):
    mock_request.return_value.status_code = 400
    with pytest.raises(FormatValidationError):
        alerce.query_objects(format="not_allowed_format")


@patch.object(Session, "request")
def test_query_objects_format_pandas(mock_request):
    def mock_result():
        return {"items": [{"oid": "test"}]}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.query_objects(format="pandas")
    assert isinstance(r, DataFrame)


@patch.object(Session, "request")
def test_query_objects_format_pandas_index(mock_request):
    def mock_result():
        return {"items": [{"oid": "test"}]}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    index = "oid"
    r = alerce.query_objects(format="pandas", index=index)
    assert r.index.name == index


@patch.object(Session, "request")
def test_query_objects_format_pandas_sort(mock_request):
    def mock_result():
        return {"items": [{"mjd": 2}, {"mjd": 1}]}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    sort = "mjd"
    r = alerce.query_objects(format="pandas", sort=sort)
    assert r.mjd.iloc[0] < r.mjd.iloc[1]


@patch.object(Session, "request")
def test_query_objects_format_json(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = "ok"
    r = alerce.query_objects(format="json")
    assert r == "ok"


@patch.object(Session, "request")
def test_query_objects_format_csv(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = [
        {"oid": 1, "mjd": 2},
        {"oid": 3, "mjd": 4},
    ]
    r = alerce.query_objects(format="csv")
    expected_csv = "oid,mjd\n1,2\n3,4\n"
    assert r == expected_csv


@patch.object(Session, "request")
def test_query_objects_format_votable(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"items": {}}
    r = alerce.query_objects(format="votable")
    assert isinstance(r, Table)


@patch.object(Session, "request")
def test_query_object(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_object("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_lightcurve(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_lightcurve("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_detections(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_detections("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_non_detections(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_non_detections("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_magstats(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_magstats("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_probabilities(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_probabilities("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_features(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_features("oid")
    assert r is not None


@patch.object(Session, "request")
def test_query_single_feature(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_feature(oid="oid", name="feature")
    assert r is not None


@patch.object(Session, "request")
def test_query_classifiers(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_classifiers()
    assert r is not None


@patch.object(Session, "request")
def test_query_classes(mock_request):
    mock_request.return_value.status_code = 200
    r = alerce.query_classes("lc_classifier", "bulk_0.0.1")
    assert r is not None

@patch.object(Session, "request")
def test_query_detections(mock_request):
    def mock_result():
        return [
            {"candid":"candid1","tid":"ztf","sid":None,"aid":None,"pid":1234,"oid":"oid"},
            {"candid":"candid2","tid":"ztf","sid":None,"aid":None,"pid":1234,"oid":"oid"}
        ]
    
    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result

    r = alerce.query_forced_photometry("oid")
    assert r is not None