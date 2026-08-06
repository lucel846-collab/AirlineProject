from src.exporter import export_csv
from src.logger import logger
from src.master_data import MasterData
from src.normalizer import Normalizer
from src.paths import INPUT_FILE, OUTPUT_FILE
from src.reader import read_excel
from src.validator import Validator


class FlightConverter:
    def __init__(self):
        self.master = MasterData()
        self.normalizer = Normalizer(self.master)
        self.validator = Validator(self.master)

    def run(self):

        logger.info("▽変換開始▽")
        df = read_excel(INPUT_FILE)
    
        self.master.load() 
        self.normalizer.normalize_airport(df)
        result = self.validator.validate(df)
        if result.has_errors:
            result.export()
            return
        self.normalizer.add_airline_name(df)
        self.normalizer.add_route(df)

        export_csv(df, OUTPUT_FILE)
        logger.info("△変換完了△")

  
if __name__ == "__main__":
     FlightConverter().run()

