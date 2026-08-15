from src.handlers.basehandler import BaseHandler
from src.normalizer import DailyNormalizer
from src.validator import CommonValidator, DailyValidator


class DailyFlightHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = DailyNormalizer(master)
        self.validator = DailyValidator(master)
