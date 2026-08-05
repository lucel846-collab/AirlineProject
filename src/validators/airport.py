import pandas as pd
from src.master_data import MasterData
from src.validator_result import ValidationResult


def validate_airport_alias(df: pd.DataFrame, master: MasterData, result: ValidationResult) -> None:
    for column in ("出発空港", "到着空港", "到着予定空港"):
        for index, value in df[column].items():
            if not pd.isna(value) and value != "" and not master.exists_airport_alias(value):
                result.add_error(
                    index=index,
                    column=column,
                    value=value,
                    message=f"{column}コードがエイリアスマスタに存在しません"
                )
