from src.exporter import export_csv
from src.logger import logger
from src.master_data import MasterData
from src.normalizer import Normalizer
from src.paths import INPUT_FILE, OUTPUT_FILE
from src.reader import read_excel
from src.validator import Validator


def main():

    logger.info("変換開始")
    df = read_excel(INPUT_FILE)

    master = MasterData()
    normalizer = Normalizer(master)
    validator = Validator(master)

    master.load() 
    normalizer.normalize_airport(df)
    result = validator.validate(df)
    if result.has_errors:
        result.export()
        return
    normalizer.add_airline_name(df)
    normalizer.add_route(df)

    export_csv(df, OUTPUT_FILE)
    logger.info("変換完了")

  
if __name__ == "__main__":
    main()
