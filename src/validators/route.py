import pandas as pd
from src.validators.adderror import add_error


def validate_route_alias(df: pd.DataFrame, route_alias_dict: dict[tuple[str, str, str], str], errors: list[dict[str, any]]) -> None:

    for index, row in df.iterrows():
        key = (
            row["航空会社"],
            row["事業所"],
            f"{row['出発空港']}{row['到着空港']}"
        )
        if key not in route_alias_dict:
            add_error(
                errors,
                index,
                "路線コード",
                f"{row['航空会社']}-{row['事業所']}-{row['出発空港']}{row['到着空港']}",
                "路線コードがエイリアスマスタに存在しません"
            )

