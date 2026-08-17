from src.handlers.basehandler import BaseHandler
from src.normalizer import ForeignCargoNormalizer
from src.validator import CommonValidator, ForeignCargoValidator


class ForeignCargoHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = ForeignCargoNormalizer(master)
        self.validator = ForeignCargoValidator(master)

