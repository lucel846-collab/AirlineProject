import pandas as pd
from src.validator_result import ValidationResult

# 運航区分
VALID_OPERATION_TYPES = {
    "SD(定期)",
    "XD(DVT)",
    "ND(CHRT)",
    "ND(臨時)",
}

def validate_operation_type(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for index, value in df["運航区分"].items():

        if value not in VALID_OPERATION_TYPES:

            ValidationResult.add_error(
                errors,
                index,
                "運航区分",
                value,
                "値が不正です"
            )

def validate_seat_count(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for index, row in df.iterrows():

        if row["座席数"] < row["旅客数"]:

            ValidationResult.add_error(
                errors,
                index,
                "座席数",
                row["座席数"],
                "旅客数以下です"
            )


def validate_dvt_arrival(df: pd.DataFrame, errors: list[dict[str, any]] ) -> None:

    for index, row in df.iterrows():

        if row["運航区分"] == "XD(DVT)" and (
            pd.isna(row["到着予定空港"]) or str(row["到着予定空港"]).strip() == ""
        ):
            ValidationResult.add_error(
                errors,
                index,
                "到着予定空港",
                row["到着予定空港"],
                "XD(DVT)では必須です"
            )

def validate_cancelled_flights(df: pd.DataFrame, errors:list[dict[str, any]]) -> None:

    CANCELLED_FLIGHT_CHECK_COLUMNS = [
    "座席数",
    "旅客数",
    "INF",
    "貨物重量",
    "メール重量",
]
    for index,row in df.iterrows():
        if row["便名"] in [ "CXL", "CNL"]:
            for col in CANCELLED_FLIGHT_CHECK_COLUMNS:
                if row[col] !=0:
                    ValidationResult.add_error(
                        errors,
                        index,
                        col,
                        row[col],
                        "CXL/CNLの場合は0である必要があります。"
                    )
