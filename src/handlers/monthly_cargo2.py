from src.handlers.basehandler import BaseHandler
from src.normalizers.monthlycargonormalizer import MonthlyCargoNormalizer
from src.validators.validatorset_common import CommonValidator
from src.validators.validatorset_monthlycargo2 import MonthlyCargoValidator2


class MonthlyCargoHandler2(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = MonthlyCargoNormalizer(master)
        self.validator = MonthlyCargoValidator2(master)

