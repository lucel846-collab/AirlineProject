from src.handlers.basehandler import BaseHandler
from src.normalizer import Normalizer_Monthly
from src.validator import Validator_Common, Validator_Monthly


class MonthlyRouteHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = Validator_Common(master)
        self.normalizer = Normalizer_Monthly(master)
        self.validator = Validator_Monthly(master)

