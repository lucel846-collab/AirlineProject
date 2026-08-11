from src.handlers.basehandler import BaseHandler
from src.normalizer import Normalizer_Daily_Route
from src.validator import Validator_Common, Validator_Daily_Route


class DailyRouteHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = Validator_Common(master)
        self.normalizer = Normalizer_Daily_Route(master)
        self.validator = Validator_Daily_Route(master)

