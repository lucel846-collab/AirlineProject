import pandas as pd
from src.master_data import MasterData
from src.validators.validator_result import ValidationResult


def validate_airline_code(df: pd.DataFrame, master: MasterData, result: ValidationResult) -> None:

    for index, value in df["航空会社"].items():
        if not master.exists_airline_code(value.strip()):
            result.add_error(
                filenm=df.attrs.get("filename"),
                index=index,
                column="航空会社",
                value=value,
                message="航空会社コードがマスタに存在しません"
            )  

