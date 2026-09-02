import pandas as pd

from src.master_data import MasterData
from src.validators.validator_result import ValidationResult


def validate_route_alias_routecode(df: pd.DataFrame, master: MasterData,result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    valid_operation_types = {
        "SD(定期)",
        "SI(定期)",
        "XD(臨時)",
        "XI(臨時)",
    }
    for index, row in df.iterrows():
        key = (
            row["航空会社"],
            row["事業所"],
            f"{row['出発空港']}{row['到着空港']}"
            )
        if row["運航区分"] in valid_operation_types and not master.exists_route_alias(*key):
            result.add_error(
                filenm=filename,
                index=index,
                column="路線コード",
                value=f"{row['航空会社']}-{row['事業所']}-{row['出発空港']}{row['到着空港']}",
                message="路線コードがエイリアスマスタに存在しません"
            )

def validate_route_alias_routecode2(df: pd.DataFrame, master: MasterData,result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index, row in df.iterrows():
        key = (
            row["航空会社"],
            row["事業所"],
            f"{row['相手先空港']}{row['事業所']}"
            )
        if  row['相手先空港'] != "CTS" and  not master.exists_route_alias(*key):
            result.add_error(
                filenm=filename,
                index=index,
                column="路線コード",
                value=f"{row['航空会社']}-{row['事業所']}-{row['相手先空港']}{row['事業所']}",
                message="路線コードがエイリアスマスタに存在しません"
            )


def validate_route_alias_routename(df: pd.DataFrame, master: MasterData,result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index, row in df.iterrows():
        key = (
            row["航空会社"],
            row["事業所"],
            row['路線名']
            )
        if not master.exists_route_alias(*key):
            result.add_error(
                filenm=filename,
                index=index,
                column="路線名",
                value=f"{row['航空会社']}-{row['事業所']}-{row['路線名']}",
                message="路線コードがエイリアスマスタに存在しません"
            )
