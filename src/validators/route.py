import pandas as pd
from src.master_data import MasterData
from src.validator_result import ValidationResult


def validate_route_alias(df: pd.DataFrame, master: MasterData, errors: list[dict[str, any]]) -> None:

    for index, row in df.iterrows():
        key = (
            row["航空会社"],
            row["事業所"],
            f"{row['出発空港']}{row['到着空港']}"
        )
        if not master.exists_route_alias(*key):
            ValidationResult.add_error(
                errors,
                index,
                "路線コード",
                f"{row['航空会社']}-{row['事業所']}-{row['出発空港']}{row['到着空港']}",
                "路線コードがエイリアスマスタに存在しません"
            )

