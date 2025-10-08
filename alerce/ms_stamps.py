import warnings
import gzip
import io
from .utils import Client
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
            "difference": "cutoutDifference",
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

    def _get_first_detection(self, survey, oid):
        """
        Kwargs must have:

        survey: ztf | lsst
        oid: some_oid

        Kwargs may have:

        measurement_id: some_measurement_id

        """
        detections = self.search_client.query_detections(survey, oid, format="pandas")

        # TODO: adapt API to retrieve has_stamp for lsst
        first_detection = detections[detections.has_stamp].mjd.astype("int64").min()

        # Este try debe cambiarse por una deteccion de error de mjd.
        try:
            first_detection = int(first_detection)
        except TypeError:
            raise CandidError()
        return first_detection

    def _check_survey_validity(self, survey):
        if survey == "ztf":
            warnings.warn(
                "ZTF is not yet supported in the stamp multisurvey API.", UserWarning
            )
            raise NotImplementedError(
                "ZTF is not yet supported in the multisurvey API."
            )
        if survey not in VALID_SURVEYS:
            raise ValueError(f"survey must be one of {VALID_SURVEYS}")

    def multisurvey_plot_stamps(self, survey, oid, candid=None, **kwargs):
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

        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        if candid is not None:
            params["candid"] = candid
        params.update(kwargs)

        oid = kwargs.get("oid")
        survey = kwargs.get("survey_id")

        if kwargs.get("measurement_id"):
            measurement_id = kwargs.get("measurement_id")
        else:
            measurement_id = self._get_first_detection(survey, oid)

        avro_url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_stamp"]

        science_url = create_stamp_parameters(
            oid, survey, measurement_id, self.ztf_types["science"], avro_url, "plot"
        )
        template_url = create_stamp_parameters(
            oid, survey, measurement_id, self.ztf_types["template"], avro_url, "plot"
        )
        difference_url = create_stamp_parameters(
            oid, survey, measurement_id, self.ztf_types["difference"], avro_url, "plot"
        )

        if not self._in_ipynb():
            warnings.warn("This method only works on Notebooks", RuntimeWarning)
            return

        images = create_html_stamp_display(
            oid, survey, measurement_id, science_url, template_url, difference_url
        )
        display(HTML(images))

    def multisurvey_get_stamps(
        self, survey, oid, candid=None, format="HDUList", **kwargs
    ):
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

        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid, "format": format}
        if candid is not None:
            params["candid"] = candid
        params.update(kwargs)

        out_format = format

        if kwargs.get("measurement_id"):
            measurement_id = kwargs.get("measurement_id")
        else:
            measurement_id = self._get_first_detection(survey, oid)

        if kwargs.get("include_variance_and_mask"):
            include_variance_and_mask = kwargs.get("include_variance_and_mask")
        else:
            include_variance_and_mask = False

        avro_url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_stamp"]

        try:
            stamp_types = [
                self.ztf_types["science"],
                self.ztf_types["template"],
                self.ztf_types["difference"],
            ]
            stamp_list = []

            for stamp_type in stamp_types:

                url = create_stamp_parameters(
                    oid, survey, measurement_id, stamp_type, avro_url, "get"
                )
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

                if include_variance_and_mask:
                    stamp_list.append(tmp_hdulist)
                else:
                    stamp_list.append(tmp_hdulist[0])

            if out_format == "HDUList":
                hdudict = {}
                for stamp, stamp_type in zip(stamp_list, stamp_types):
                    hdudict[stamp_type] = stamp
                return hdudict
            elif out_format == "numpy":
                return [stamp.data.copy() for stamp in stamp_list]

        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None

    def multisurvey_get_avro(self, survey, oid, candid=None, **kwargs):
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

        self._check_survey_validity(survey)
        params = {"survey_id": survey, "oid": oid}
        if candid is not None:
            params["candid"] = candid
        params.update(kwargs)

        measurement_id = kwargs.get("measurement_id")

        if measurement_id is None:
            measurement_id = self._get_first_detection(survey, oid)

        try:
            url = self.config["STAMP_URL"] + self.config["AVRO_ROUTES"]["get_avro"]
            params = {"oid": kwargs.get("oid"), "measurement_id": measurement_id}
            http_response = self.session.request("GET", url, params=params)
            return http_response.content
        except HTTPError:
            warnings.warn("AVRO File not found.", RuntimeWarning)
            return None
