from src.error_report import export_validation_errors
from src.exporter import export_csv
from src.logger import logger
from src.master_data import MasterData
from src.normalize1 import normalize1
from src.normalize2 import normalize2
from src.paths import ERROR_FILE, INPUT_FILE, OUTPUT_FILE
from src.reader import read_excel
from src.validator import validate


def main():

    logger.info("変換開始")
    df = read_excel(INPUT_FILE)
    master = MasterData()
    master.load() 
    normalize1(df, master.airport_alias_dict)
    errors = validate(df,  
                      master.airline_master,  
                      master.route_alias_dict, 
                      master.airport_alias_dict
                      )
    if errors:

        export_validation_errors(errors, ERROR_FILE)

        logger.error(f"{len(errors)}件のエラーがあります。")
        logger.info("ValidationError.csv を確認してください。")

        return
    normalize2(df, 
               master.route_alias_dict, 
               master.route_code_dict
               )
    export_csv(df, OUTPUT_FILE)
    logger.info("変換完了")

  
if __name__ == "__main__":
    main()
