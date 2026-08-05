import pandas as pd
from src.master_data import MasterData
from src.validator_result import ValidationResult


def validate_route_alias(df: pd.DataFrame, master: MasterData,result: ValidationResult) -> None:

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

