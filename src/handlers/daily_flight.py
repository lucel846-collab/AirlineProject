from src.handlers.basehandler import BaseHandler
from src.normalizer import Normalizer_Daily
from src.validator import CommonValidator, DailyValidator


class DailyFlightHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = Normalizer_Daily(master)
        self.validator = DailyValidator(master)
