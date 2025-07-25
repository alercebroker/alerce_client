from .utils import Client

from .ms_search_utils import configs, survey_urls_routes

VALID_SURVEYS = ["lsst", "ztf"]

class AlerceSearchMultistream(Client):
    def __init__(self, survey='ztf', **kwargs):
        self.survey = survey
        self.survey_urls_routes = survey_urls_routes

        if survey not in configs:
            raise ValueError(f"Survey '{survey}' no soportado. Usar: {list(configs.keys())}")
        
        default_config = configs[survey]
        default_config.update(kwargs)
        super().__init__(**default_config)

    @property
    def survey_url(self):
        return self.config[f"{self.survey_urls_routes[self.survey].get('api')}"]

    def _get_survey_url(self, resource, *args):
        return self.survey_url + self.config[f"{self.survey_urls_routes[self.survey].get('route')}"][resource]
    
    def check_survey_id(self, params):

        if not params.get("survey_id", None) in VALID_SURVEYS:
            raise Exception(f'survey_id: {params.get("survey_id", None)} not in {VALID_SURVEYS}')

    def query_objects_multisurvey(self, format="json", index=None, sort=None, **kwargs):
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

            q = self._request(
                "GET",
                url=self._get_survey_url("objects"),
                params=kwargs,
                result_format=format,
                response_field="items",
            )
            return q.result(index, sort)

    def query_object_multisurvey(self, format="json", **kwargs):
        """
        Gets a single object by object id

        Parameters
        ----------
        **kwargs
            Keyword arguments. Each argument can be one of the `ALERCE ZTF API`_
            object query parameters.

            - oid : str
            - survey_id : str

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'

        """

        self.check_survey_id(kwargs)

        q = self._request(
            "GET", 
            url=self._get_survey_url("single_object"),
            params=kwargs,
            result_format=format,
            response_field="items"
        )
        return q.result()

    def query_lightcurve_multisurvey(self, format="json", **kwargs):
        """
        Gets the lightcurve (detections and non_detections) of a given object

        Parameters
        ----------
        **kwargs
            Keyword arguments.

            - oid : str
            - survey_id : str

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'

        """

        self.check_survey_id(kwargs)
        q = self._request(
            "GET", 
            url=self._get_survey_url("lightcurve"),
            params=kwargs,
            result_format=format,
            response_field="items"
        )
        return q.result()

    def query_detections_multisurvey(self, format="json", index=None, sort=None, **kwargs):
        """
        Gets all detections of a given object

        Parameters
        ----------
        **kwargs
            Keyword arguments.

            - oid : str
            - survey_id : str

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        index : str
            The name of the column to use as index when format is 'pandas'
        sort : str
            The name of the column to sort when format is 'pandas'
        """

        self.check_survey_id(kwargs)
        
        q = self._request(
            "GET",
            url=self._get_survey_url("detections"),
            params=kwargs,
            result_format=format,
            response_field="items"

        )
        return q.result(index, sort)

    def query_non_detections_multisurvey(self, format="json", index=None, sort=None, **kwargs):
        """
        Gets all non detections of a given object

        Parameters
        ----------
        **kwargs
            Keyword arguments

            - oid : str
            - survey_id : str

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """

        self.check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("non_detections"),
            params=kwargs,
            result_format=format,
            response_field="items"
        )
        return q.result(index, sort)

    def query_forced_photometry_multisurvey(self,format="json", index=None, sort=None, **kwargs):
        """
        Gets all forced photometry epochs of a given object

        Parameters
        ----------
        **kwargs
            Keyword arguments

            - oid : str
            - survey_id : str

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """

        self.check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("forced_photometry"),
            params=kwargs,
            result_format=format,
            response_field="items"
        )

        return q.result(index, sort)

    def query_magstats_multisurvey(self, oid, format="json", index=None, sort=None):
        """
        Gets magnitude statistics of a given object

        Parameters
        ----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request("GET", self._get_survey_url("magstats", oid), result_format=format)
        return q.result(index, sort)

    def query_probabilities_multisurvey(self, oid, format="json", index=None, sort=None):
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
            "GET", self._get_survey_url("probabilities", oid), result_format=format
        )
        return q.result(index, sort)

    def query_features_multisurvey(self, oid, format="json", index=None, sort=None):
        """
        Gets features of a given object

        Parameters
        -----------
        oid : str
            The object identifier
        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        q = self._request("GET", self._get_survey_url("features", oid), result_format=format)
        return q.result(index, sort)

    def query_feature_multisurvey(self, oid, name, format="json"):
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
            "GET", self._get_survey_url("single_feature", oid, name), result_format=format
        )
        return q.result()

    def query_classifiers_multisurvey(self, format="json"):
        """
        Gets all classifiers and their classes
        """
        q = self._request("GET", self._get_survey_url("classifiers"), result_format=format)
        return q.result()

    def query_classes_multisurvey(self, classifier_name, classifier_version, format="json"):
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
            self._get_survey_url("classifier_classes", classifier_name, classifier_version),
            result_format=format,
        )
        return q.result()


