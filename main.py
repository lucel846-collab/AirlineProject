from src.reader import read_excel
from src.exporter import export_csv
from src.error_report import export_validation_errors
from src.master_data import (
    read_airport_master,
    read_airline_master,
    read_route_master
)
from src.validator import validate
from src.paths import (
    INPUT_FILE,
    OUTPUT_FILE,
    ERROR_FILE,
)


def main():

    df = read_excel(INPUT_FILE)
    airline_master = read_airline_master()
    airport_master = read_airport_master()
    route_master = read_route_master()

    errors = validate(df, airport_master, airline_master, route_master)
    if errors:

        export_validation_errors(errors, ERROR_FILE)

        print(f"{len(errors)}件のエラーがあります。")
        print("ValidationError.csv を確認してください。")

        return

    export_csv(df, OUTPUT_FILE)

    print("変換完了")


if __name__ == "__main__":
    main()