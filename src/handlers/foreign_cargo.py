from src.handlers.basehandler import BaseHandler
from src.normalizers.foreigncargonormalizer import ForeignCargoNormalizer
from src.validators.validatorset_common import CommonValidator
from src.validators.validatorset_forigncargo import ForeignCargoValidator


class ForeignCargoHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = ForeignCargoNormalizer(master)
        self.validator = ForeignCargoValidator(master)

