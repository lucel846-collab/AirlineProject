from src.handlers.basehandler import BaseHandler
from src.normalizers.monthlycargonormalizer import MonthlyCargoNormalizer
from src.validators.validatorset_common import CommonValidator
from src.validators.validatorset_monthlycargo import MonthlyCargoValidator


class MonthlyCargoHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = MonthlyCargoNormalizer(master)
        self.validator = MonthlyCargoValidator(master)

