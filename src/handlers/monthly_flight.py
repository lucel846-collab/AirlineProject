from src.handlers.basehandler import BaseHandler
from src.normalizer import MonthlyNormalizer
from src.validator import CommonValidator, MonthlyValidator


class MonthlyRouteHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = MonthlyNormalizer(master)
        self.validator = MonthlyValidator(master)

