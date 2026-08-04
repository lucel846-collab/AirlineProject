import pandas as pd
from src.master_data import MasterData
from src.validators.adderror import add_error


def validate_airline_code(df: pd.DataFrame, master: MasterData, errors: list[dict[str, any]]) -> None:

    for index, value in df["航空会社"].items():
        if not master.exists_airline_code(value):
            add_error(
                errors,
                index,
                "航空会社",
                value,
                "航空会社コードがマスタに存在しません"
            )  

