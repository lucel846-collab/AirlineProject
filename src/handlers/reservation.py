from src.handlers.basehandler import BaseHandler
from src.normalizers.reservationnormalizer import DailyReservationNormalizer
from src.validators.validatorset_common import CommonValidator
from src.validators.validatorset_reservation import ReservationValidator


class ReservationHandler(BaseHandler):

    def __init__(self, master):
        super().__init__(master)
        self.common_validator = CommonValidator(master)
        self.normalizer = DailyReservationNormalizer(master)
        self.validator = ReservationValidator(master)
