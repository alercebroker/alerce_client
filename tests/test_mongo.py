from unittest.mock import patch, ANY
from requests import Session
import pandas as pd
from astropy.table import Table
import sys
import pytest

sys.path.append("..")
from alerce.core import Alerce
from alerce.exceptions import ParseError

alerce = Alerce()


@patch.object(Session, "request")
def test_findOne(mock_request):

    query = {
      "collection": "object",
      "filter": {"_id": "AL22laceaicnfejpc"},
      "projection": {
        "oid": 1,
      }
    }
    def mock_result():
        return {"document": {"oid": "test"}}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.mongo_findOne(query)

    mock_request.assert_called_with("POST", ANY, params=None, json=query, data=None)
    assert r == mock_result()


@patch.object(Session, "request")
def test_find(mock_request):

    query = {
      "collection": "object",
      "filter": {"ndet": {"$gte": 100}},
      "limit": 10,
      "projection": {
        "oid": 1,
      }
    }
    def mock_result():
        return {"documents": {"oid": "test"}}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.mongo_find(query)
    mock_request.assert_called_with("POST", ANY, params=None, json=query, data=None)
    assert r == mock_result()

@patch.object(Session, "request")
def test_aggregate(mock_request):

    query = {
        "collection": "object",
        "pipeline": [
        {
          "$match": {
            "ndet": {"$lte": 505, "$gte": 500}
          }
        },
        {
          "$group": {
            "_id": "$ndet",
            "count": { "$sum": 1 }
          }
        },
        {
         "$sort": { "count": 1 }
        }
        ]
    }
    def mock_result():
        return {"document": {"_id": 500, "count" : 10}}

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.mongo_aggregate(query)
    mock_request.assert_called_with("POST", ANY, params=None, json=query, data=None)
    assert r is not None

@patch.object(Session, "request")
def test_user_error(mock_request):
    query = {
      "collection": "object",
      "filter": {"_id": "AL22laceaicnfejpc"},
      "projection": {
        "oid": 1,
      }
    }
    message = "An error with the API occurred"
    def mock_result():
        return {"message": message}

    mock_request.return_value.status_code = 400
    mock_request.return_value.json = mock_result
    with pytest.raises(ParseError) as error:
        r = alerce.mongo_find(query)
    assert error.value.message == message

@patch.object(Session, "request")
def test_query_format_pandas(mock_request):
    query = {
      "collection": "object",
      "filter": {"ndet": {"$gte": 100}},
      "limit": 10,
      "projection": {
        "oid": 1,
      }
    }
    result = {"documents": {"oid": "test"}}
    expected_df = pd.DataFrame(["test"], columns=["oid"])

    def mock_result():
        return result

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.mongo_find(query, format="pandas")
    assert isinstance(r, pd.DataFrame)
    assert r.equals(expected_df)
