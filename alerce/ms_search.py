from .utils import Client

from ms_search_utils import configs, survey_urls_routes

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
        return self.config[f"{self.survey_urls_routes[self.survey]["api"]}"]

    def __get_survey_url(self, resource, *args):
        return self.survey_url + self.config[f"{self.survey_urls_routes[self.survey]["route"]}"][resource] % args


