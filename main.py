import glob
import os

from src.exporter import export_csv
from src.logger import logger
from src.master_data import MasterData
from src.normalizer import Normalizer
from src.paths import INPUT_DIR, OUTPUT_DIR
from src.reader import read_excel
from src.validator import Validator


class FlightConverter:
    def __init__(self):
        self.master = MasterData()
        self.normalizer = Normalizer(self.master)
        self.validator = Validator(self.master)

    def run(self):

        logger.info("▽変換開始▽")
        self.master.load() 
        file_paths = glob.glob(f"{INPUT_DIR}/*.xlsx")
        for file_path in file_paths:
            df = read_excel(file_path)
            self.normalizer.normalize_airport(df)
            result = self.validator.validate(df)
            if result.has_errors:
                result.export()
                return
            self.normalizer.add_airline_name(df)
            self.normalizer.add_route(df)
            file_out_path = OUTPUT_DIR / os.path.basename(file_path).replace(".xlsx", ".csv")
            export_csv(df, file_out_path)   
            logger.info("△変換完了△")
  
if __name__ == "__main__":
     FlightConverter().run()

