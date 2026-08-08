import pandas as pd
from src.detect_layout import detect_layout
from src.master_data import MasterData
from src.validator_result import ValidationResult


def validate_route_alias(df: pd.DataFrame, master: MasterData,result: ValidationResult) -> None:
    layout = detect_layout(df)
    if layout== "DAILY_FLIGHT":
        for index, row in df.iterrows():
            key = (
                row["航空会社"],
                row["事業所"],
                f"{row['出発空港']}{row['到着空港']}"
                )
            if not master.exists_route_alias(*key):
                result.add_error(
                    index=index,
                    column="路線コード",
                    value=f"{row['航空会社']}-{row['事業所']}-{row['出発空港']}{row['到着空港']}",
                    message="路線コードがエイリアスマスタに存在しません"
                )

    elif layout == "MONTHLY_ROURTE":
        for index, row in df.iterrows():
            key = (
                row["航空会社"],
                row["事業所"],
                row['路線名']
                )
            if not master.exists_route_alias(*key):
                result.add_error(
                    index=index,
                    column="路線コード",
                    value=f"{row['航空会社']}-{row['事業所']}-{row['路線名']}",
                    message="路線コードがエイリアスマスタに存在しません"
                )
