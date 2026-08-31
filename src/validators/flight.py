import pandas as pd

from src.validators.validator_result import ValidationResult

# 運航区分
VALID_OPERATION_DAILY_TYPES = {
    "SD(定期)",
    "SI(定期)",
    "XD(DVT)",
    "XI(DVT)",
    "ND(CHRT)",
    "NI(CHRT)",
    "XD(臨時)",
    "XI(臨時)",
    "ND(周遊)",
}

# 運航区分
VALID_OPERATION_MONTHLY_TYPES = {
    "SD(定期)",
    "SI(定期)",
    "ND(CHRT)",
    "NI(CHRT)",
}

VALID_OPERATION_IRREGAL_TYPES = {
    "XD(DVT)",
    "XI(DVT)",
    "ND(CHRT)",
    "NI(CHRT)",
    "ND(周遊)",
}

VALID_OPERATION_FOREIGN_CARGO_TYPES = {
    "SI(定期)",
    "NI(CHRT)",
    "NI(保税)",
}

# 必須列名
CANCELLED_FLIGHT_CHECK_COLUMNS = [
    "座席数",
    "旅客数",
    "INF数",
    "貨物重量",
    "メール重量",
]
# --- 共通ロジック関数 ---
def validate_operation_base(df:pd.DataFrame, result: ValidationResult,required_columns: list[str]) -> None:
    filename = df.attrs.get("filename")
    for index, value in df["運航区分"].items():
        if value not in required_columns:
            result.add_error(
                filenm=filename,
                index=index,
                column="運航区分",
                value=value,
                message="値が不正です"
            )

def validate_operation_daily_type(df: pd.DataFrame, _master,result: ValidationResult) -> None:
    validate_operation_base(df, result, VALID_OPERATION_DAILY_TYPES)

def validate_operation_monthly_type(df: pd.DataFrame, _master,result: ValidationResult) -> None:
    validate_operation_base(df, result,  VALID_OPERATION_MONTHLY_TYPES)

def validate_operation_irregal_type(df: pd.DataFrame, _master,result: ValidationResult) -> None:
    validate_operation_base(df, result,VALID_OPERATION_IRREGAL_TYPES)
    
def validate_operation_foreign_cargo_type(df: pd.DataFrame, _master,result: ValidationResult) -> None:
    validate_operation_base(df, result, VALID_OPERATION_FOREIGN_CARGO_TYPES)

def validate_seat_count(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index, row in df.iterrows():
        if isinstance(row["座席数"], (int, float)) and isinstance(row["旅客数"], (int, float)) and row["座席数"] < row["旅客数"]:
                result.add_error(
                    filenm=filename,
                    index=index,
                    column="座席数",
                    value={"旅客数": row["旅客数"], "座席数": row["座席数"]},
                    message="座席数より旅客数が超過しています"
                )

def validate_operation_attributes(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index, row in df.iterrows():
        if row["運航区分"] == "XD(DVT)" and (
            pd.isna(row["到着予定空港"]) or str(row["到着予定空港"]).strip() == ""
        ):
            result.add_error(
                filenm=filename,
                index=index,
                column="到着予定空港",
                value=row["到着予定空港"],
                message="XD(DVT)では「到着予定空港」が必須です"
            )

        elif row["運航区分"] == "ND(周遊)" and (
            not(pd.isna(row["出発空港"]) or pd.isna(row["到着空港"])) 
            and (str(row["出発空港"]).strip() != str(row["到着空港"]).strip())
        ):
            result.add_error(
                filenm=filename,
                index=index,
                column="到着空港",
                value=row["到着空港"],
                message="ND(周遊)では到着空港と出発空港は同一です"
            )

        elif row["運航区分"] == "NI(保税)" and not(
            pd.isna(row["相手先空港"])  and  str(row["到着空港"]).strip() =="" 
        ):
            result.add_error(
                filenm=filename,
                index=index,
                column="相手先空港",
                value=row["相手先空港"],
                message="NI(保税)では相手先空港は記載不要です"
            )

def validate_cancelled_flights(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index,row in df.iterrows():
        if row["便名"] in [ "CXL", "CNL"]:
            for col in CANCELLED_FLIGHT_CHECK_COLUMNS:
                if row[col] !=0:
                    result.add_error(
                        filenm=filename,
                        index=index,
                        column=col,
                        value=row[col],
                        message="CXL/CNLの場合は0である必要があります。"
                    )
