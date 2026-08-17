from src.handlers.basehandler import BaseHandler
from src.normalizers.monthlycargonormalizer import MonthlyCargoNormalizer
from src.validators.commonvalidator import CommonValidator
from src.validators.monthlycargovalidator import MonthlyCargoValidator


class MonthlyCargoHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = MonthlyCargoNormalizer(master)
        self.validator = MonthlyCargoValidator(master)

