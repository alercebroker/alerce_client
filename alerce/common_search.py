from .ztf_search import ZTFSearch
from .ms_search import AlerceSearchMultiSurvey
from .utils import Client

# Problemas con esta solucion, el manejo de los kwargs
# para cada cliente es diferente, y no se pueden mezclar
#   Se puede normalizar esto -> agregar kwars en cada cliente 
#   si lo usa bien, pero que no falle por agregarlos
# ademas de que no todos los clientes tienen los mismos metodos
#   Se puede hacer un catch de los metodos que no existan

class CommonSearch(Client):

    def __init__(self, **kwargs):
        ztf_config = kwargs.get("ztf_config", {})
        lsst_config = kwargs.get("lsst_config", {})
        self.surveys_clients = {
            "ztf": ZTFSearch(ztf_config),
            "lsst": AlerceSearchMultiSurvey(lsst_config),
        }

    def query_objects(self, survey_id, format="pandas", index=None, sort=None, **kwargs):
       return self.surveys_clients[survey_id].query_objects(format=format, index=index, sort=sort, **kwargs)
    
    def query_object(self, survey_id, oid, format="json"):
        return self.surveys_clients[survey_id].query_object(oid, format=format)

    def query_lightcurve(self, survey_id, oid, format="json"):
        return self.surveys_clients[survey_id].query_lightcurve(oid, format=format)

    def query_detections(self, survey_id, oid, format="json", index=None, sort=None):
        return self.surveys_clients[survey_id].query_detections(oid, format=format, index=index, sort=sort)

    def query_non_detections(self, survey_id, oid, format="json", index=None, sort=None):
        return self.surveys_clients[survey_id].query_non_detections(oid, format=format, index=index, sort=sort)

    def query_forced_photometry(self, survey_id, oid, format="json", index=None, sort=None):
        return self.surveys_clients[survey_id].query_forced_photometry(oid, format=format, index=index, sort=sort)

    def query_magstats(self, survey_id, oid, format="json", index=None, sort=None):
        return self.surveys_clients[survey_id].query_magstats(oid, format=format, index=index, sort=sort)

    def query_probabilities(self, survey_id, oid, format="json", index=None, sort=None):
        return self.surveys_clients[survey_id].query_probabilities(oid, format=format, index=index, sort=sort)

    def query_features(self, survey_id, oid, format="json", index=None, sort=None):
        return self.surveys_clients[survey_id].query_features(oid, format=format, index=index, sort=sort)

    def query_feature(self, survey_id, oid, name, format="json"):
        return self.surveys_clients[survey_id].query_feature(oid, name, format=format)

    def query_classifiers(self, survey_id, format="json"):
        return self.surveys_clients[survey_id].query_classifiers(format=format)

    def query_classes(self, survey_id, classifier_name, classifier_version, format="json"):
        return self.surveys_clients[survey_id].query_classes(classifier_name, classifier_version, format=format)
