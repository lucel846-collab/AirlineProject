import pandas as pd
from src.master_data import MasterData
from src.validators.adderror import add_error


def validate_airport_alias(df: pd.DataFrame, master: MasterData, errors: list[dict[str, any]]) -> None:
    for column in ("出発空港", "到着空港", "到着予定空港"):
        for index, value in df[column].items():
            if not pd.isna(value) and value != "" and not master.exists_airport_alias(value):
                add_error(
                    errors,
                    index,
                    column,
                    value,
                    f"{column}コードがエイリアスマスタに存在しません"
                )
