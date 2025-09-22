from .utils import Client
from .ztf_search import AlerceZtfSearch
from .lsst_search import AlerceLsstSearch


class AlerceSearch(Client):

    def __init__(self):
        
        self.ztf = AlerceZtfSearch()
        self.lsst = AlerceLsstSearch()

    def _get_survey(self, params):
        return params.get("survey_id")

    def query_objects(self, **kwargs):
    
        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_objects(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_objects(**kwargs)

    def query_object(self, **kwargs):
       
        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_object(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_object(**kwargs)

    def query_lightcurve(self, **kwargs):

        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_lightcurve(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_lightcurve(**kwargs)

    def query_detections(self, **kwargs):

        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_detections(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_detections(**kwargs)
      
    def query_non_detections(self, **kwargs):

        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_non_detections(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_non_detections(**kwargs)

    def query_forced_photometry(self, **kwargs):

        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_forced_photometry(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_forced_photometry(**kwargs)
      
    def query_magstats(self, **kwargs):

        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_magstats(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_magstats(**kwargs)
       
    def query_probabilities(self, **kwargs):

        if self._get_survey(kwargs) == "ztf":
            kwargs.pop('survey_id')
            return self.ztf.ztf_query_probabilities(**kwargs)
        elif self._get_survey(kwargs) == "lsst":
            return self.lsst.lsst_query_probabilities(**kwargs)