import pandas as pd
from src.validators.adderror import add_error


def validate_airport_alias(df: pd.DataFrame, airport_alias_dict: dict[str, str], errors: list[dict[str, any]]) -> None:
    for column in ("出発空港", "到着空港"):
        for index, value in df[column].items():
            if value not in airport_alias_dict:
                add_error(
                    errors,
                    index,
                    column,
                    value,
                    f"{column}コードがエイリアスマスタに存在しません"
                )
