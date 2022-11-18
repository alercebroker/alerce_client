from unittest.mock import Mock, patch
from requests import Session
from requests import Response
from pandas import DataFrame
from astropy.table import Table
import sys
import pytest

sys.path.append("..")
from alerce.core import Alerce
from alerce.exceptions import ParseError

alerce = Alerce()

@patch.object(Session, "request")
def test_select(mock_request):
    def mock_result():
        return b'oid,g,mjd\n1,15.5,5650'

    mock_request.return_value.status_code = 200
    mock_request.return_value.content = mock_result
    query = 'SELECT * from objects;'
    r = alerce.send_query(query)
    assert r is not None

@patch.object(Session, "request")
def test_empty(mock_request):
    def mock_result():
        return b'oid,g,mjd\n'
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = mock_result
    query = 'SELECT * from objects where oid=-1;'
    r = alerce.send_query(query)
    assert r == b'oid,g,mjd\n'

@patch.object(Session, "request")
def test_typo(mock_request):
    message = b'syntax error at or near "SLECT"\nLINE 1: SLECT * FROM objects;\n        ^\n'
    def mock_result():
        return message
    mock_request.return_value.status_code = 400
    mock_request.return_value.content = mock_result
    query = 'SLECT * FROM OBJECTS;'
    r = alerce.send_query(query)
    with pytest.raises(ParseError) as error:
        r = alerce.send_query(query)
    assert error.message == message.decode('utf-8')

@patch.object(Session, "request")
def test_permission(mock_request):
    message = b"permission denied\n"
    def mock_result():
        return message
    mock_request.return_value.status_code = 400
    mock_request.return_value.data = mock_result
    query = "DELETE FROM objects WHERE id=1"
    r = alerce.send_query(query)
    with pytest.raises(ParseError) as error:
        r = alerce.send_query(query)
    assert error.message == message.decode('utf-8')

@patch.object(Session, "request")
def test_query_format_csv(mock_request):
    result = 'oid,g,mjd\n1,15.5,5650\n'
    def mock_result():
        return result.encode('utf-8')
    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.send_query(format="csv")
    assert r == result

@patch.object(Session, "request")
def test_query_format_pandas(mock_request):
    result = 'oid,g,mjd\n1,15.5,5650\n'
    def mock_result():
        return result.encode('utf-8')

    mock_request.return_value.status_code = 200
    mock_request.return_value.json = mock_result
    r = alerce.query_objects(format="pandas")
    assert isinstance(r, DataFrame)

@patch.object(Session, "request")
def test_query_format_error(mock_request):
    mock_request.return_value.status_code = 400
    with pytest.raises(FormatValidationError):
        alerce.query_objects(format="json")

