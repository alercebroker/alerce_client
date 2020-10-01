import json

import requests

from .exceptions import FormatValidationError, ParseError, handle_error
from .utils import Result, Client


class AlerceSearch(Client):
    def __init__(self, **kwargs):
        self.session = requests.Session()
        default_config = {
            "ZTF_API_URL": "http://3.212.59.238:8082",
            "ZTF_ROUTES": {
                "objects": "/objects",
                "single_object": "/objects/%s",
                "detections": "/objects/%s/detections",
                "non_detections": "/objects/%s/non_detections",
                "lightcurve": "/objects/%s/lightcurve",
                "magstats": "/objects/%s/magstats",
                "probabilities": "/objects/%s/probabilities",
                "features": "/objects/%s/features",
                "single_feature": "/objects/%s/features/%s",
            },
        }
        default_config.update(kwargs)
        super().__init__(**default_config)
        

    @property
    def ztf_url(self):
        return self.config["ZTF_API_URL"]

    def __get_url(self, resource, *args):
        return self.ztf_url + self.config["ZTF_ROUTES"][resource] % args

    def __validate_format(self, format):
        format = format.lower()
        if not format in self.allowed_formats:
            raise FormatValidationError(
                "Format '%s' not in %s" % (format, self.allowed_formats), code=500
            )
        return format

    def query_objects(self, format="pandas", index=None, sort=None, **kwargs):
        """
        Gets a list of objects filtered by specified parameters.
        It is strongly advised to look at the documentation of `ALERCE ZTF API`_

        Parameters
        ----------
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        index : str
            Name of the column to use as index when format is 'pandas'
        sort : str
            Name of the column to sort when format is 'pandas'
       
        **kwargs
            Keyword arguments. Each argument can be one of the `ALERCE ZTF API`_
            object query parameters.

            - classifier : str
                classifier name
            - class_name : str
                class name
            - ndet : int[]
                Range of detections.
            - probability : float
                Minimum probability.
            - firstmjd : float[]
                First detection date range in mjd.
            - lastmjd : float[]
                Last detection date range in mjd.
            - ra : float
                Ra in degrees for conesearch.
            - dec : float
                Dec in degrees for conesearch.
            - radius : float
                Radius in arcsec for conesearch.
            - page : int
                Page or offset to retrieve. Default value : 1
            - page_size : int
                Number of objects to retrieve in each page. Default value: 10
            - count : str (bool like)
                Whether to count total objects or not. Can be a string representation of boolean
                like "True", "true", "yes", "false", ...
            - order_by : str
                Column used for ordering. Available values : oid, ndethist, ncovhist, mjdstarthist, mjdendhist, corrected, stellar, ndet, g_r_max, g_r_max_corr, g_r_mean, g_r_mean_corr, meanra, meandec, sigmara, sigmadec, deltamjd, firstmjd, lastmjd, step_id_corr, object, classifier_name, class_name, probability, probabilities
            - order_mode : str
                Ordering could be ascendent or descendent.
                Available values : ASC, DESC
        """

        if "class_name" in kwargs:
            kwargs["class"] = kwargs.pop("class_name")
        q = self._request(
            "GET",
            url=self.__get_url("objects"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )
        return q.result(index, sort)

    def query_object(self, oid, format="json"):
        """
        Gets a single object by object id

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'

        """
        q = self._request(
            "GET", self.__get_url("single_object", oid), result_format=format
        )
        return q.result()

    def query_lightcurve(self, oid, format="json"):
        """
        Gets the lightcurve (detections and non_detections) of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'

        """
        q = self._request(
            "GET", self.__get_url("lightcurve", oid), result_format=format
        )
        return q.result()

    def query_detections(self, oid, format="json", index=None, sort=None):
        """
        Gets all detections of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'
        """
        q = self._request(
            "GET", self.__get_url("detections", oid), result_format=format
        )
        return q.result(index, sort)

    def query_non_detections(self, oid, format="json", index=None, sort=None):
        """
        Gets all non detections of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request(
            "GET", self.__get_url("non_detections", oid), result_format=format
        )
        return q.result(index, sort)

    def query_magstats(self, oid, format="json", index=None, sort=None):
        """
        Gets magnitude statistics of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request("GET", self.__get_url("magstats", oid), result_format=format)
        return q.result(index, sort)

    def query_probabilities(self, oid, format="json", index=None, sort=None):
        """
        Gets probabilities of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request(
            "GET", self.__get_url("probabilities", oid), result_format=format
        )
        return q.result(index, sort)

    def query_features(self, oid, format="json", index=None, sort=None):
        """
        Gets features of a given object

        Parameters
        -----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request("GET", self.__get_url("features", oid), result_format=format)
        return q.result(index, sort)

    def query_feature(self, oid, name, format="json"):
        """
        Gets a single feature of a specified object id

        Parameters
        ----------
        oid : str
            The object identifier
        name : str
            The feature's name
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request(
            "GET", self.__get_url("single_feature", oid, name), result_format=format
        )
        return q.result()
