from unittest.mock import Mock, patch
import pytest
from requests import Session
import sys

sys.path.append("..")
from alerce.core import Alerce
from alerce.exceptions import APIError
from catshtm_testcases import *


def test_catshtm_conesearch_all(requests_mock):
    alerce = Alerce()
    requests_mock.register_uri(
        "GET",
        alerce.config["CATSHTM_API_URL"]
        + alerce.config["CATSHTM_ROUTES"]["conesearch_all"],
        json=CONESEARCH_ALL_RESPONSE,
    )
    r = alerce.catshtm_conesearch(
        ra=357.73373, dec=14.20514, radius=10, format="pandas", catalog_name="all"
    )
    assert r is not None


def test_catshtm_conesearch_catalog(requests_mock):
    alerce = Alerce()
    requests_mock.register_uri(
        "GET",
        alerce.config["CATSHTM_API_URL"]
        + alerce.config["CATSHTM_ROUTES"]["conesearch"],
        json=CONESEARCH_CATALOG_RESPONSE,
    )
    r = alerce.catshtm_conesearch(
        ra=357.73373, dec=14.20514, radius=10, format="pandas", catalog_name="2MASS"
    )
    assert r is not None


def test_catshtm_crossmatch_all(requests_mock):
    alerce = Alerce()
    requests_mock.register_uri(
        "GET",
        alerce.config["CATSHTM_API_URL"]
        + alerce.config["CATSHTM_ROUTES"]["crossmatch_all"],
        json=COSSMATCH_ALL_RESPONSE,
    )
    r = alerce.catshtm_crossmatch(
        ra=357.73373, dec=14.20514, radius=10, format="pandas", catalog_name="all"
    )
    assert r is not None


def test_catshtm_crossmatch_catalog(requests_mock):
    alerce = Alerce()
    requests_mock.register_uri(
        "GET",
        alerce.config["CATSHTM_API_URL"]
        + alerce.config["CATSHTM_ROUTES"]["crossmatch"],
        json=CROSSMATCH_CATALOG_RESPONSE,
    )
    r = alerce.catshtm_crossmatch(
        ra=357.73373, dec=14.20514, radius=10, format="pandas", catalog_name="2MASS"
    )
    assert r is not None


def test_error(requests_mock):
    alerce = Alerce()
    requests_mock.register_uri("GET", "mock://test.com", status_code=500)
    with pytest.raises(APIError):
        alerce._request_catshtm("GET", "mock://test.com")


def test_catshtm_redshift(requests_mock):
    alerce = Alerce()
    requests_mock.register_uri(
        "GET",
        alerce.config["CATSHTM_API_URL"]
        + alerce.config["CATSHTM_ROUTES"]["crossmatch_all"],
        json=COSSMATCH_ALL_RESPONSE,
    )
    r = alerce.catshtm_redshift(ra=357.73373, dec=14.20514, radius=10)
    assert r is not None
