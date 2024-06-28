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
def test_select(mock_request):
    result = b"oid,g,mjd\n1,15.5,5650"

    def mock_result(encoding):
        return result.decode(encoding)

    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode = mock_result
    query = "SELECT * from objects;"
    r = alerce.send_query(query)

    mock_request.assert_called_with("POST", ANY, params=None, data={"query": query})
    assert r is not None


@patch.object(Session, "request")
def test_empty(mock_request):
    result = b"oid,g,mjd\n"

    def mock_result(encoding):
        return result.decode(encoding)

    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode = mock_result
    query = "SELECT * from objects where oid=-1;"
    r = alerce.send_query(query)
    assert r == result.decode("utf-8")


@patch.object(Session, "request")
def test_typo(mock_request):
    message = (
        b'syntax error at or near "SLECT"\nLINE 1: SLECT * FROM objects;\n        ^\n'
    )

    def mock_result(encoding):
        return message.decode(encoding)

    mock_request.return_value.status_code = 400
    mock_request.return_value.content.decode = mock_result
    query = "SLECT * FROM OBJECTS;"
    with pytest.raises(ParseError) as error:
        r = alerce.send_query(query)
    print(message)
    print(error.value.message)
    assert error.value.message == message.decode("utf-8")


@patch.object(Session, "request")
def test_permission(mock_request):
    message = b"permission denied\n"

    def mock_result(encoding):
        return message.decode(encoding)

    mock_request.return_value.status_code = 400
    mock_request.return_value.content.decode = mock_result
    query = "DELETE FROM objects WHERE id=1"
    with pytest.raises(ParseError) as error:
        r = alerce.send_query(query)
    assert error.value.message == message.decode("utf-8")


@patch.object(Session, "request")
def test_query_format_csv(mock_request):
    result = b"oid,g,mjd\n1,15.5,5650\n"

    def mock_result(encoding):
        return result.decode(encoding)

    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode = mock_result
    query = "SELECT * FROM objects;"
    r = alerce.send_query(query, format="csv")
    assert r == result.decode("utf-8")


@patch.object(Session, "request")
def test_query_format_pandas(mock_request):
    result = b"oid,g,mjd\n1,15.5,5650\n"

    def mock_result(encoding):
        return result.decode(encoding)

    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode = mock_result
    query = "SELECT * FROM objects;"
    r = alerce.send_query(query, format="pandas")
    assert isinstance(r, pd.DataFrame)
    assert r.to_csv(index=False) == result.decode("utf-8")


@patch.object(Session, "request")
def test_query_format_pandas_sort(mock_request):
    def mock_result(encoding):
        return "mjd\n2\n1\n"

    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode = mock_result
    sort = "mjd"
    r = alerce.send_query("", format="pandas", sort=sort)
    assert r.mjd.iloc[0] < r.mjd.iloc[1]


@patch.object(Session, "request")
def test_query_format_pandas_index(mock_request):
    def mock_result(encoding):
        return "oid,oid,mjd\ntest,test,1\n"

    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode = mock_result
    index = "oid"
    r = alerce.send_query("", format="pandas", index=index)
    assert r.index.name == index


@patch.object(Session, "request")
def test_query_format_votable(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode.return_value = "mjd,oid,oid\n1,5,5\n"
    r = alerce.send_query("", format="votable")
    columns = ["mjd", "oid", "oid_1"]
    expected_table = Table([[1], [5], [5]], names=columns)
    assert isinstance(r, Table)
    for row_result, row_expected in zip(
        r.iterrows(*columns), expected_table.iterrows(*columns)
    ):
        assert row_expected == row_result

    assert r == expected_table


@patch.object(Session, "request")
def test_query_format_error(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content.decode.return_value = (
        "mjd,oid,oid\n1,5,5\n2,6,6\n"
    )
    r = alerce.send_query("", format="json")
    expected_result = '[{"mjd":1,"oid":5,"oid_1":5},{"mjd":2,"oid":6,"oid_1":6}]'
    assert r == expected_result


def test_init():
    api_url = "test.alece"
    db_api_url = "db.test.alerce"
    alerce_test = Alerce(ZTF_API_URL=api_url, ZTF_DB_API_URL=db_api_url)
    assert alerce_test.config["ZTF_DB_API_URL"] == db_api_url
    assert alerce_test.config["ZTF_API_URL"] == api_url


def test_init_json():
    api_url = "test.alece"
    db_api_url = "db.test.alerce"
    test_config = {"ZTF_API_URL": api_url, "ZTF_DB_API_URL": db_api_url}
    alerce_test = Alerce()
    alerce_test.load_config_from_object(test_config)
    assert alerce_test.config["ZTF_DB_API_URL"] == db_api_url
    assert alerce_test.config["ZTF_API_URL"] == api_url
