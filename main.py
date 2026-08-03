from src.error_report import export_validation_errors
from src.exporter import export_csv
from src.logger import logger
from src.master_data import (
    load_airport_alias_dict,
    load_route_alias_dict,
    load_route_code_dict,
    read_airline_master,
)
from src.normalize1 import normalize1
from src.normalize2 import normalize2
from src.paths import ERROR_FILE, INPUT_FILE, OUTPUT_FILE
from src.reader import read_excel
from src.validator import validate


def main():

    logger.info("変換開始")
    df = read_excel(INPUT_FILE)
    logger.info("マスタファイルを読み込みます。")
    # Validationで使用するDataFrame
    airline_master = read_airline_master()
    # 高速検索用の辞書
    route_alias_dict = load_route_alias_dict()
    airport_alias_dict = load_airport_alias_dict()
    route_code_dict = load_route_code_dict()

    logger.info("ファイル正規化開始")
    normalize1(df, airport_alias_dict)
    logger.info("ファイルチェック開始")
    errors = validate(df,  airline_master,  route_alias_dict, airport_alias_dict)
    if errors:

        export_validation_errors(errors, ERROR_FILE)

        logger.error(f"{len(errors)}件のエラーがあります。")
        logger.info("ValidationError.csv を確認してください。")

        return
    logger.info("ルートコード追加開始")
    normalize2(df, route_alias_dict,route_code_dict)
    logger.info("CSV出力開始")
    export_csv(df, OUTPUT_FILE)
    logger.info("変換完了")


if __name__ == "__main__":
    main()