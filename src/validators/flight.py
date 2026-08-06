import pandas as pd
from src.validator_result import ValidationResult

# 運航区分
VALID_OPERATION_TYPES = {
    "SD(定期)",
    "XD(DVT)",
    "ND(CHRT)",
    "XD(臨時)",
    "ND(周遊)",
}
# 必須列名
CANCELLED_FLIGHT_CHECK_COLUMNS = [
    "座席数",
    "旅客数",
    "INF",
    "貨物重量",
    "メール重量",
]

def validate_operation_type(df: pd.DataFrame, result: ValidationResult) -> None:

    for index, value in df["運航区分"].items():

        if value not in VALID_OPERATION_TYPES:

            result.add_error(
                index=index,
                column="運航区分",
                value=value,
                message="値が不正です"
            )

def validate_seat_count(df: pd.DataFrame, result: ValidationResult) -> None:

    for index, row in df.iterrows():

        if row["座席数"] < row["旅客数"]:

            result.add_error(
                index=index,
                column="座席数",
                value=row["座席数"],
                message="旅客数以下です"
            )


def validate_operation_attributes(df: pd.DataFrame, result: ValidationResult) -> None:

    for index, row in df.iterrows():

        if row["運航区分"] == "XD(DVT)" and (
            pd.isna(row["到着予定空港"]) or str(row["到着予定空港"]).strip() == ""
        ):
            result.add_error(
                index=index,
                column="到着予定空港",
                value=row["到着予定空港"],
                message="XD(DVT)では必須です"
            )

        if row["運航区分"] == "ND(周遊)" and not(
            pd.isna(row["出発空港"]) and str(row["出発空港"]).strip() == str(row["到着空港"]).strip()
        ):
            result.add_error(
                index=index,
                column="到着空港",
                value=row["到着空港"],
                message="ND(周遊)では到着空港と出発空港は同一です"
            )

def validate_cancelled_flights(df: pd.DataFrame, result: ValidationResult) -> None:

    for index,row in df.iterrows():
        if row["便名"] in [ "CXL", "CNL"]:
            for col in CANCELLED_FLIGHT_CHECK_COLUMNS:
                if row[col] !=0:
                    result.add_error(
                        index=index,
                        column=col,
                        value=row[col],
                        message="CXL/CNLの場合は0である必要があります。"
                    )
