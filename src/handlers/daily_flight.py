from src.handlers.basehandler import BaseHandler
from src.normalizers.dailynormalizer import DailyNormalizer
from src.validators.commonvalidator import CommonValidator
from src.validators.dailyvalidator import DailyValidator


class DailyFlightHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = DailyNormalizer(master)
        self.validator = DailyValidator(master)
