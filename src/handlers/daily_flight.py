from src.handlers.basehandler import BaseHandler
from src.normalizers.dailynormalizer import DailyNormalizer
from src.validators.validatorset_common import CommonValidator
from src.validators.validatorset_daily import DailyValidator


class DailyFlightHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = DailyNormalizer(master)
        self.validator = DailyValidator(master)
