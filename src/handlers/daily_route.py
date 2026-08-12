from src.handlers.basehandler import BaseHandler
from src.normalizer import Normalizer_Daily_Route
from src.validator import CommonValidator, DailyRouteValidator


class DailyRouteHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = Normalizer_Daily_Route(master)
        self.validator = DailyRouteValidator(master)

