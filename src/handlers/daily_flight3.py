from src.handlers.basehandler import BaseHandler
from src.normalizers.dailynormalizer import DailyNormalizer
from src.validators.commonvalidator import CommonValidator
from src.validators.dailyvalidator3 import DailyValidator3


class DailyFlightHandler3(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = DailyNormalizer(master)
        self.validator = DailyValidator3(master)
