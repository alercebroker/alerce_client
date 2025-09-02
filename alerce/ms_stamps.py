import warnings
import gzip
import io
from .utils import Client
from astropy.io.fits import HDUList
from astropy.io.fits import open as fits_open
from urllib.error import HTTPError
from alerce.ms_search import AlerceSearchMultiSurvey
from alerce.exceptions import CandidError
from .ms_stamp_utils import create_html_stamp_display, create_stamp_parameters
from IPython.display import HTML, display
from .config import stamp_config

VALID_SURVEYS = ["lsst", "ztf"]

class AlerceStampsMultisurvey(Client):
    search_client = AlerceSearchMultiSurvey()

    def __init__(self, **kwargs):
        stamp_config.update(kwargs)

        self.ztf_types = {
            "science": "cutoutScience",
            "template": "cutoutTemplate",
            "difference": "cutoutDifference"
        }

        super().__init__(**stamp_config)

    def _in_ipynb(self):
        try:
            from IPython import get_ipython
            import os

            if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
                raise ImportError("console")
                return False
            if "VSCODE_PID" in os.environ:  # pragma: no cover
                raise ImportError("vscode")
                return False
        except Exception as e:
            return False
        else:  # pragma: no cover
            return True

    def _get_first_detection(self, **kwargs): 

        """
        Kwargs must have:

        survey: ztf | lsst
        oid: some_oid

        Kwargs may have:

        measurement_id: some_measurement_id
        
        """
        detections = self.search_client.multisurvey_query_detections(**kwargs, format="pandas")
        first_detection = detections[detections.has_stamp].mjd.astype("int64").min()

        # Este try debe cambiarse por una deteccion de error de mjd.
        try:
            first_detection = int(first_detection) 
        except TypeError:
            raise CandidError()
        return first_detection
    
    def _check_survey_id(self, params):
            
        self.survey = self._get_survey_param(params)

        if not self.survey in VALID_SURVEYS:
            raise Exception(
                f'survey_id: {params.get("survey_id", None)} not in {VALID_SURVEYS}'
            )

    def multisurvey_plot_stamps(self, **kwargs):
        """
        Plot stamp in a notebook given oid and survey, measurement_id is optional. It uses IPython HTML.

        Parameters
        ----------
        oid (Required) : :py:class:`str`
            object ID in ALeRCE DBs.

        survey (Required): ztf or lsst
        
        measurement_id (optional) : :py:class:`int`
            measurement_id of the avro to be downloaded.

        Returns
        -------
            Display the stamps on a jupyter notebook.
        """
        
        self._check_survey_id(kwargs)

        oid = kwargs.get("oid")
        survey = kwargs.get("survey_id")
        if kwargs.get("measurement_id"):
            measurement_id = kwargs.get("measurement_id")
        else:
            measurement_id = self._get_first_detection(**kwargs)


        avro_url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_stamp"]

        science_url = create_stamp_parameters(oid, survey, measurement_id, self.ztf_types["science"], avro_url, 'plot')
        template_url = create_stamp_parameters(oid, survey, measurement_id, self.ztf_types["template"], avro_url, 'plot')
        difference_url = create_stamp_parameters(oid, survey, measurement_id, self.ztf_types["difference"], avro_url, 'plot')

        if not self._in_ipynb():
            warnings.warn("This method only works on Notebooks", RuntimeWarning)
            return
        
        images = create_html_stamp_display(oid, survey, measurement_id, science_url, template_url, difference_url)
        display(HTML(images))

    def multisurvey_get_stamps(self, **kwargs):
        """Download Stamps for an specific alert given oid and survey, measurement_id is optional.

        Parameters
        ----------
        oid (Required) : :py:class:`str`
            object ID in ALeRCE DBs.

        survey (Required): ztf or lsst
        
        measurement_id (optional) : :py:class:`int`
            measurement_id of the avro to be downloaded.

        format : :py:class: `str`
            Output format [HDUList|numpy]

        Returns
        -------
            Science, Template and Difference stamps for an specific alert.
        """

        self._check_survey_id(kwargs)

        oid = kwargs.get("oid")
        survey = kwargs.get("survey_id")

        if kwargs.get("measurement_id"):
            measurement_id = kwargs.get("measurement_id")
        else:
            measurement_id = self._get_first_detection(**kwargs)

        avro_url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_stamp"]

        try:
            stamp_types = [self.ztf_types["science"], self.ztf_types["template"], self.ztf_types["difference"]]
            stamp_list = []
            for stamp_type in stamp_types:

                url = create_stamp_parameters(oid, survey, measurement_id, stamp_type, avro_url, 'get')

                http_response = self.session.request("GET", url)
                if survey == "ztf":
                    fits_buffer = gzip.open(io.BytesIO(http_response.content))
                elif survey == "lsst":
                    fits_buffer = io.BytesIO(http_response.content)
                else:
                    raise Exception(f"survey {survey} not valid")

                tmp_hdulist = fits_open(
                    io.BytesIO(fits_buffer.read()), ignore_missing_simple=True
                )

                stamp_list.append(tmp_hdulist[0])

            if format == "HDUList":
                hdulist = HDUList()
                for stamp, stamp_type in zip(stamp_list, stamp_types):
                    stamp.header["STAMP_TYPE"] = stamp_type
                    hdulist.append(stamp)
                return hdulist
            elif format == "numpy":
                return [stamp.data.copy() for stamp in stamp_list]
        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None

    def multisurvey_get_avro(self, **kwargs):
        """Download avro of some alert given oid and survey, measurement_id is optional.

        Parameters
        ----------
        oid (Required) : :py:class:`str`
            object ID in ALeRCE DBs.

        survey (Required): ztf or lsst
        
        measurement_id (optional) : :py:class:`int`
            measurement_id of the avro to be downloaded.

        Returns
        -------
            Avro of a given alert.
        """

        self._check_survey_id(kwargs)

        measurement_id = kwargs.get("measurement_id")

        if measurement_id is None:
            measurement_id = self._get_first_detection(**kwargs)

        try:
            url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_avro"]
            params = {"oid": kwargs.get("oid"), "measurement_id": measurement_id}
            http_response = self.session.request("GET", url, params=params)
            return http_response.content
        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None
