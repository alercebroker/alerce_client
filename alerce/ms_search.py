from .utils import Client

from .config import configs


VALID_SURVEYS = ["lsst", "ztf"]

class AlerceSearchMultiSurvey(Client):
    def __init__(self, **kwargs):

        default_config = configs
        default_config.update(kwargs)
        super().__init__(**default_config)

        self.url_ms = self.config["multisurvey"]["URL_MS"]
        self.routes_ms = self.config["multisurvey"]["ROUTES_MS"]

        ####################################################################

        # # Rutas de prueba para local
        # self.url_local = self.config["local"]["URL_LOCAL"]
        # self.routes_local = self.config["local"]["ROUTES_LOCAL"]

        ####################################################################
    def _get_survey_url(self, resource):
        return (
            self.url_ms + self.routes_ms[resource] 
           #self.url_local + self.routes_local[resource] # Descomentar esto para probar en local (y comentar lo de arriba)
        )
        
    def _get_survey_param(self, params):
        return params.get("survey_id") or params.get("survey")

    def _check_survey_id(self, params):
            
        self.survey = self._get_survey_param(params)

        if not self.survey in VALID_SURVEYS:
            raise Exception(
                f'survey_id: {params.get("survey_id", None)} not in {VALID_SURVEYS}'
            )

    def multisurvey_query_objects(self, format="json", index=None, sort=None, **kwargs):
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

        self._check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("objects"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )
        return q.result(index, sort)

    def multisurvey_query_object(self, format="json", **kwargs):
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

        self._check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("single_object"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )
        return q.result()

    def multisurvey_query_lightcurve(self, format="json", **kwargs):
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

        self._check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("lightcurve"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )
        return q.result()

    def multisurvey_query_detections(
        self, format="json", index=None, sort=None, **kwargs
    ):
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
        self._check_survey_id(kwargs)


        q = self._request(
            "GET",
            url=self._get_survey_url("detections"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )
        return q.result(index, sort)

    def multisurvey_query_non_detections(
        self, format="json", index=None, sort=None, **kwargs
    ):
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

        self._check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("non_detections"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )
        return q.result(index, sort)

    def multisurvey_query_forced_photometry(
        self, format="json", index=None, sort=None, **kwargs
    ):
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

        self._check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("forced_photometry"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )

        return q.result(index, sort)
    
    def multisurvey_query_probabilities(self, format="json", index=None, sort=None, **kwargs):
        """
        Gets probabilities of a given object

        Parameters
        ----------
        **kwargs
            Keyword arguments

            - oid (required) : str
            - classifier (optional) : str 

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        url = self._get_survey_url("probabilities")

        q = self._request(
            "GET",
            url=url,
            params=kwargs,
            result_format=format,
            response_field="items",
        )

        return q.result(index, sort)
    
    def multisurvey_query_magstats(self, format="json", index=None, sort=None, **kwargs):
        """
        Gets magnitude statistics of a given object

        Parameters
        ----------
        **kwargs
            Keyword arguments

            - oid : str
            - survey_id : str

        format : str
            Return format. Can be one of 'pandas' | 'votable' | 'json'
        """
        self._check_survey_id(kwargs)

        q = self._request(
            "GET",
            url=self._get_survey_url("magstats"),
            params=kwargs,
            result_format=format,
            response_field="items",
        )

        return q.result(index, sort)