from src.handlers.basehandler import BaseHandler
from src.normalizer import Normalizer_Daily
from src.validator import Validator_Common, Validator_Daily


class DailyFlightHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = Validator_Common(master)
        self.normalizer = Normalizer_Daily(master)
        self.validator = Validator_Daily(master)
