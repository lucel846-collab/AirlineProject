class BaseHandler:

    def __init__(self, master):
        self.master = master
        self.common_validator = None
        self.normalizer = None
        self.validator = None

    def process(self, df):

        self.normalizer.normalize_airport(df)
        
        result = self.common_validator.validate(df)
        if result.has_errors:
            return result

        result = self.validator.validate(df)
        if result.has_errors:
            return result

        self.normalizer.add_airline_name(df)
        self.normalizer.add_route(df)

        return result