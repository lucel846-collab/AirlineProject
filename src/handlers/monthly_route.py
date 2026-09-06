from src.handlers.basehandler import BaseHandler
from src.normalizers.monthlynormalizer import MonthlyNormalizer
from src.validators.validatorset_common import CommonValidator
from src.validators.validatorset_monthly import MonthlyValidator


class MonthlyRouteHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = MonthlyNormalizer(master)
        self.validator = MonthlyValidator(master)

