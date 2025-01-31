from .utils import Client


class AlerceSearch(Client):
    def __init__(self, **kwargs):
        default_config = {
            "ZTF_API_URL": "https://api.alerce.online",
            "ZTF_V1_ROUTE_PREFIX": "/ztf/v1",
            "ZTF_V1_ROUTES": {
                "objects": "/objects",
                "single_object": "/objects/%s",
                "magstats": "/objects/%s/magstats",
                "probabilities": "/objects/%s/probabilities",
                "features": "/objects/%s/features",
                "single_feature": "/objects/%s/features/%s",
                "classifiers": "/classifiers",
                "classifier_classes": "/classifiers/%s/%s/classes",
            },
            "V2_ROUTE_PREFIX": "/v2/lightcurve",
            "V2_ROUTES": {
                "detections": "/detections/%s",
                "non_detections": "/non_detections/%s",
                "lightcurve": "/lightcurve/%s",
            },
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

    @property
    def ztf_v1_url(self):
        return self.config["ZTF_API_URL"] + self.config["ZTF_V1_ROUTE_PREFIX"]

    @property
    def v2_url(self):
        return self.config["ZTF_API_URL"] + self.config["V2_ROUTE_PREFIX"]

    def __get_url(self, resource, *args):
        if resource in self.config["V2_ROUTES"]:
            return self.v2_url + self.config["V2_ROUTES"][resource] % args
        else:
            return self.ztf_v1_url + self.config["ZTF_V1_ROUTES"][resource] % args

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
        print(self.__get_url("objects"))
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
        print(self.__get_url("detections", oid))
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

    def query_forced_photometry(self, oid, format="json", index=None, sort=None):
        """
        Gets all forced photometry epochs of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request(
            "GET",
            "https://api.alerce.online/v2/lightcurve/forced-photometry/%s" % oid,
            result_format=format,
        )

        # NOTA: la api principal de ztf no tiene ruta de forced photometry, la v2 si tiene. Esto es lo mas facil
        # pero no es correcto.

        # all this extra code is to expand the extra fields.
        complete_result = q.result(index, sort)

        FIELDS_TO_REMOVE = ["extra_fields", "aid", "sid"]

        if format == "json":
            parsed_result = []
            for result in complete_result:
                new_result = result.copy()
                extra_fields = new_result.pop("extra_fields", {})
                for f_t_r in FIELDS_TO_REMOVE:
                    new_result.pop(f_t_r, None)
                new_result.update(extra_fields)
                parsed_result.append(new_result)
        if format == "pandas" or format == "csv":
            import pandas as pd

            if len(complete_result) == 0:
                # early exit the object dont have any fp
                return pd.DataFrame()
            else:
                extra_fields = complete_result["extra_fields"].copy()
                complete_result = complete_result.drop(columns=FIELDS_TO_REMOVE)
                # expand
                extra_fields = pd.json_normalize(extra_fields)
                # merge
                parsed_result = complete_result.merge(extra_fields)
                if format == "csv":
                    parsed_result = parsed_result.to_csv(index=False)

        return parsed_result

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

    def query_classifiers(self, format="json"):
        """
        Gets all classifiers and their classes
        """
        q = self._request("GET", self.__get_url("classifiers"), result_format=format)
        return q.result()

    def query_classes(self, classifier_name, classifier_version, format="json"):
        """
        Gets classes from a specified classifier

        Parameters
        ----------

        classifier_name : str
            The classifier unique name
        classifier_version : str
            The classifier's version
        """
        q = self._request(
            "GET",
            self.__get_url("classifier_classes", classifier_name, classifier_version),
            result_format=format,
        )
        return q.result()
