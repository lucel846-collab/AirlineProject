from src.normalizer import Normalizer_Daily_Route
from src.validator import Validator_Common, Validator_Daily_Route


class DailyRouteHandler:

    def __init__(self, master):
        self.validatorCommon = Validator_Common(master)
        self.normalizer = Normalizer_Daily_Route(master)
        self.validator = Validator_Daily_Route(master)

    def process(self, df):
        self.normalizer.normalize_airport(df)

        result = self.validatorCommon.validate(df)
        if result.has_errors:
            return result

        result = self.validator.validate(df)
        if result.has_errors:
            return result

        self.normalizer.add_airline_name(df)
        self.normalizer.add_route(df)

        return result