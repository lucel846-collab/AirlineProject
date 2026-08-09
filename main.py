import glob
import os

from src.detect_layout import Layout_type, detect_layout
from src.exporter import export_csv
from src.logger import logger
from src.master_data import MasterData
from src.normalizer import (
    Normalizer_Daily,
    Normalizer_Daily_route,
    Normalizer_Monthly,
)
from src.paths import INPUT_DIR, OUTPUT_DIR
from src.reader import read_excel
from src.validator import (
    Validator_Daily,
    Validator_Daily_Route,
    Validator_Monthly,
)


class FlightConverter:
    def __init__(self):
        self.master = MasterData()
        self.normalizer_daily = Normalizer_Daily(self.master)
        self.validator_daily = Validator_Daily(self.master)
        self.normalizer_monthly = Normalizer_Monthly(self.master)
        self.validator_monthly = Validator_Monthly(self.master)
        self.normalizer_daily_route = Normalizer_Daily_route(self.master)
        self.validator_daily_route = Validator_Daily_Route(self.master)

    def run(self):

        logger.info("▽変換開始▽")
        self.master.load() 
        file_paths = glob.glob(f"{INPUT_DIR}/*.xlsx")
        for file_path in file_paths:
            df = read_excel(file_path)
            layout =detect_layout(df)
            if layout == Layout_type.DAILY_FLIGHT.value:
                logger.info(layout)
                self.normalizer_daily.normalize_airport(df)
                result = self.validator_daily.validate(df)
                if result.has_errors:
                    result.export()
                    return
                self.normalizer_daily.add_airline_name(df)
                self.normalizer_daily.add_route(df)

            elif layout == Layout_type.MONTHLY_ROUTE.value:
                logger.info(layout)
                self.normalizer_monthly.normalize_airport(df)
                result = self.validator_monthly.validate(df)
                if result.has_errors:
                    result.export()
                    return
                self.normalizer_monthly.add_airline_name(df)
                self.normalizer_monthly.add_route(df)

            elif layout == Layout_type.DAILY_ROUTE.value:
                logger.info(layout)
                self.normalizer_daily_route.normalize_airport(df)
                result = self.validator_daily_route.validate(df)
                if result.has_errors:
                    result.export()
                    return
                self.normalizer_daily_route.add_airline_name(df)
                self.normalizer_daily_route.add_route(df)


            file_out_path = OUTPUT_DIR / os.path.basename(file_path).replace(".xlsx", ".csv")
            export_csv(df, file_out_path)   
            logger.info("△変換完了△")
  
if __name__ == "__main__":
     FlightConverter().run()

