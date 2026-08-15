import pandas as pd
from src.master_data import MasterData
from src.validator_result import ValidationResult


def validate_airport_alias(df: pd.DataFrame, master: MasterData, result: ValidationResult) -> None:
    for column in ("出発空港", "到着空港"):
        for index, value in df[column].items():
            if not pd.isna(value) and value != "" and not master.exists_airport_alias(value):
                result.add_error(
                    filenm=df.attrs.get("filename"),
                    index=index,
                    column=column,
                    value=value,
                    message=f"{column}コードがエイリアスマスタに存在しません"
                )
def validate_airport_alias2(df: pd.DataFrame, master: MasterData, result: ValidationResult) -> None:
    for index, value in df["到着予定空港"].items():
        if not pd.isna(value) and value != "" and not master.exists_airport_alias(value):
            result.add_error(
                filenm=df.attrs.get("filename"),
                index=index,
                column="到着予定空港",
                value=value,
                message="到着予定空港コードがエイリアスマスタに存在しません"
            )

def validate_airport_office(df: pd.DataFrame, master: MasterData,result: ValidationResult) -> None:
    for index, value in df["事業所"].items():
        if not pd.isna(value) and value != "" and not master.exists_airport_office(value):
            result.add_error(
                filenm=df.attrs.get("filename"),
                index=index,
                column="事業所",
                value=value,
                message="事業所コードが不正です"
            )

