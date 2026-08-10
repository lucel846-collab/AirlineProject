from src.normalizer import Normalizer_Daily
from src.validator import Validator_Common, Validator_Daily


class DailyFlightHandler:

    def __init__(self, master):
        self.CommonValidator = Validator_Common(master)
        self.normalizer = Normalizer_Daily(master)
        self.validator = Validator_Daily(master)

    def process(self, df):
        self.normalizer.normalize_airport(df)

        result = self.CommonValidator.validate(df)
        if result.has_errors:
            return result

        result = self.validator.validate(df)
        if result.has_errors:
            return result

        self.normalizer.add_airline_name(df)
        self.normalizer.add_route(df)

        return result