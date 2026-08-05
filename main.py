from src.error_report import export_validation_errors
from src.exporter import export_csv
from src.logger import logger
from src.master_data import MasterData
from src.normalizer import Normalizer
from src.paths import ERROR_FILE, INPUT_FILE, OUTPUT_FILE
from src.reader import read_excel
from src.validator import validate


def main():

    logger.info("変換開始")
    df = read_excel(INPUT_FILE)
    master = MasterData()
    master.load() 
    normalizer = Normalizer(master)
    normalizer.normalize_airport(df)
    errors = validate(df,master) 
    if errors:

        export_validation_errors(errors, ERROR_FILE)

        logger.error(f"{len(errors)}件のエラーがあります。")
        logger.info("ValidationError.csv を確認してください。")

        return
    normalizer.add_airline_name(df)
    normalizer.add_route(df)
    export_csv(df, OUTPUT_FILE)
    logger.info("変換完了")

  
if __name__ == "__main__":
    main()
