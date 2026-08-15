from src.handlers.basehandler import BaseHandler
from src.normalizer import MonthlyCargoNormalizer
from src.validator import CommonValidator, MonthlyCargoValidator


class MonthlyCargoHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = MonthlyCargoNormalizer(master)
        self.validator = MonthlyCargoValidator(master)

