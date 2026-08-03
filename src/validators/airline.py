import pandas as pd
from src.validators.adderror import add_error


def validate_airline_code(df: pd.DataFrame, airline_master_df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    airline_codes = set(airline_master_df["AirlineCD"])
    for index, value in df["航空会社"].items():
        if value not in airline_codes:
            add_error(
                errors,
                index,
                "航空会社",
                value,
                "航空会社コードがマスタに存在しません"
            )  

