from src.handlers.basehandler import BaseHandler
from src.normalizers.dailyroutenormalizer import DailyRouteNormalizer
from src.validators.commonvalidator import CommonValidator
from src.validators.dailyroutevalidator import DailyRouteValidator


class DailyRouteHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = DailyRouteNormalizer(master)
        self.validator = DailyRouteValidator(master)

