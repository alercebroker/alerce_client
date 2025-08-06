import warnings
import gzip
import io
from .utils import Client
from astropy.io.fits import HDUList
from astropy.io.fits import open as fits_open
from urllib.error import HTTPError
from alerce.ms_search import AlerceSearchMultiSurvey
from alerce.exceptions import CandidError
from ms_stamp_utils import create_html_stamp_display, create_stamp_url
from IPython.display import HTML


VALID_SURVEYS = ["lsst", "ztf"]

class AlerceStamps(Client):
    search_client = AlerceSearchMultiSurvey()

    def __init__(self, **kwargs):
        default_config = {
            "AVRO_URL": "https://avro.alerce.online",
            "AVRO_ROUTES": {"get_stamp": "/get_stamp", "get_avro": "/get_avro"},
        }
        default_config.update(kwargs)
        super().__init__(**default_config)

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
        detections = self.search_client.multisurvey_query_detections(kwargs, format="pandas")
        first_detection = detections[detections.has_stamp].candid.astype("int64").min()
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

    def plot_stamps(self, **kwargs):
        """
        Plot stamp in a notebook given oid. It uses IPython HTML.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs. (must have)
        survey: ztf or lsst (must have)

        measurement_id : :py:class:`int`
            measurement_id of the stamp to be displayed. (optional)

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
            measurement_id = self._get_first_detection(kwargs)

        science = "cutoutScience"
        template = "cutoutTemplate"
        difference = "cutoutDifference"

        if not self._in_ipynb():
            warnings.warn("This method only works on Notebooks", RuntimeWarning)
            return

        science_url = create_stamp_url(oid, survey, measurement_id, science)
        template_url = create_stamp_url(oid, survey, measurement_id, template)
        difference_url = create_stamp_url(oid, survey, measurement_id, difference)

        images = create_html_stamp_display(oid, survey, measurement_id, science_url, template_url, difference_url)
        
        display(HTML(images))

    def get_stamps(self, **kwargs):
        """Download Stamps for an specific alert.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        candid : :py:class:`int`
            Candid of the stamp to be displayed.
        format : :py:class: `str`
            Output format [HDUList|numpy]

        Returns
        -------
            Science, Template and Difference stamps for an specific alert.
        """

        self._check_survey_id(kwargs)

        if candid is None:
            candid = self._get_first_detection(kwargs)
        try:
            stamp_types = ["science", "template", "difference"]
            stamp_list = []
            for stamp_type in stamp_types:
                url = "%s?oid=%s&candid=%s&type=%s&format=fits" % (
                    self.config["AVRO_URL"] + self.config["AVRO_ROUTES"]["get_stamp"],
                    kwargs.get("oid"),
                    candid,
                    stamp_type,
                )

                http_response = self.session.request("GET", url)

                with gzip.open(io.BytesIO(http_response.content), "rb") as f:
                    tmp_hdulist = fits_open(
                        io.BytesIO(f.read()), ignore_missing_simple=True
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

    def get_avro(self, **kwargs):
        """Download avro of some alert.

        Parameters
        ----------
        oid : :py:class:`str`
            object ID in ALeRCE DBs.
        candid : :py:class:`int`
            Candid of the avro to be downloaded.

        Returns
        -------
            Avro of a given alert.
        """

        self._check_survey_id(kwargs)

        if candid is None:
            candid = self._get_first_detection(kwargs.get("oid"))
        try:
            url = self.config["AVRO_URL"] + self.config["AVRO_ROUTES"]["get_avro"]
            params = {"oid": kwargs.get("oid"), "candid": candid}
            http_response = self.session.request("GET", url, params=params)
            return http_response.content
        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None
