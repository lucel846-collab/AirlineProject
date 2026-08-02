from src.reader import read_excel
from src.exporter import export_csv
from src.error_report import export_validation_errors
from src.master_data import (
    read_airport_master,
    read_airline_master,
    read_route_master,
    load_route_alias_dict,
    load_airport_alias_dict,
)
from src.validator import validate
from src.paths import (
    INPUT_FILE,
    OUTPUT_FILE,
    ERROR_FILE,
)
from src.normalize import normalize
from src.logger import logger



def main():

    logger.info("変換開始")
    df = read_excel(INPUT_FILE)
    logger.info("マスタファイルを読み込みます。")
    airline_master = read_airline_master()
    airport_master = read_airport_master()
    route_master = read_route_master()
    route_alias_dict = load_route_alias_dict()
    airport_alias_dict = load_airport_alias_dict()

    logger.info("ファイルチェック開始")
    errors = validate(df, airport_master, airline_master, route_master, route_alias_dict, airport_alias_dict)
    if errors:

        export_validation_errors(errors, ERROR_FILE)

        logger.error(f"{len(errors)}件のエラーがあります。")
        logger.info("ValidationError.csv を確認してください。")

        return
    logger.info("CSV出力開始")
    normalize(df, route_alias_dict, airport_alias_dict)
    export_csv(df, OUTPUT_FILE)
    logger.info("変換完了")


if __name__ == "__main__":
    main()