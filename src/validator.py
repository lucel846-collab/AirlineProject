import pandas as pd
from datetime import date


# 必須列
REQUIRED_COLUMNS = [
    "運航日",
    "航空会社",
    "便名",
    "出発空港",
    "運航区分",
    "座席数",
    "旅客数",
    "貨物重量",
    "メール重量",
    "事業所",
]


# 運航区分
VALID_OPERATION_TYPES = {
    "SD(定期)",
    "XD(DVT)",
    "ND(CHRT)",
    "ND(臨時)",
}


def validate(df: pd.DataFrame, 
             airport_master_df: pd.DataFrame, 
             airline_master_df: pd.DataFrame, 
             route_master_df: pd.DataFrame,
             route_alias_dict: dict[tuple[str, str, str], str],
             airport_alias_dict: dict[str, str],
             ) -> List:
    errors = []
    validate_columns(df,errors)
    validate_required(df,errors)
    validate_operation_type(df,errors)
    validate_seat_count(df,errors)
    validate_dvt_arrival(df,errors)
    validate_Cancelled_flights(df,errors)
    validate_previous_date_check(df,errors)
    validate_airline_code(df, airline_master_df, errors)
    validate_airport_alias(df, airport_alias_dict, errors)
    validate_route_alias(df, route_alias_dict, errors)
    return errors

def add_error(errors: List, row, column, value, message) -> None:
    errors.append({"行番号":row+2,"項目名":column,"入力値":value,"エラー内容":message})

def validate_columns(df: pd.DataFrame, errors: List) -> None:

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append({"行番号":"","項目名":col,"入力値":"","エラー内容":"列が存在しません"})

 
def validate_required(df: pd.Dataframe, errors:List) -> None:

    for col in REQUIRED_COLUMNS:

        for index, value in df[col].items():

            if pd.isna(value) or str(value).strip() == "":

                add_error(
                    errors,
                    index,
                    col,
                    value,
                    "必須項目です"
                )


def validate_operation_type(df: pd.DataFrame, errors: List) -> None:
    
    for index, value in df["運航区分"].items():

        if value not in VALID_OPERATION_TYPES:

            add_error(
                errors,
                index,
                "運航区分",
                value,
                "値が不正です"
            )

def validate_seat_count(df: pd.DataFrame, errors: List) -> None:

     for index, row in df.iterrows():

        if row["座席数"] < row["旅客数"]:

            add_error(
                errors,
                index,
                "座席数",
                row["座席数"],
                "旅客数以下です"
            )


def validate_dvt_arrival(df: pd.DataFrame, errors: List) -> None:
    
    for index, row in df.iterrows():

        if row["運航区分"] == "XD(DVT)":
            if pd.isna(row["到着予定空港"]) or str(row["到着予定空港"]).strip() == "":
                add_error(
                    errors,
                    index,
                    "到着予定空港",
                    row["到着予定空港"],
                    "XD(DVT)では必須です"
                )

def validate_Cancelled_flights(df: pd.DataFrame, errors:List) -> None:
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
                    add_error(
                        errors,
                        index,
                        col,
                        row[col],
                        "CXL/CNLの場合は0である必要があります。"
                    )

def validate_previous_date_check(df: pd.DataFrame, errors:List) -> None:
    today = pd.Timestamp.today().normalize()
    first_date = today.replace(day=1)
    last_date_prev_month = first_date - pd.Timedelta(days=1)
    first_date_prev_month = last_date_prev_month.replace(day=1)
    for index,row in df.iterrows():
        if (row["運航日"] > last_date_prev_month or row["運航日"] < first_date_prev_month):
            add_error(
                errors,
                index,
                "運航日",
                row["運航日"],
                "運航日は前月である必要があります。"
            )

def validate_airline_code(df: pd.DataFrame, airline_master_df: pd.DataFrame, errors: List) -> None:

    airline_codes = set(airline_master_df["AirlineCD"])
    for index, value in df["航空会社"].items():
        if value not in airline_codes:
            add_error(
                errors,
                index,
                "航空会社",
                value,
                "航空会社コードがマスタに存在しません"
            )  

def validate_airport_alias(df: pd.DataFrame, airport_alias_dict: dict[str, str], errors: List) -> None:
    for column in ("出発空港", "到着空港"):
        for index, value in df[column].items():
            if value not in airport_alias_dict:
                add_error(
                    errors,
                    index,
                    column,
                    value,
                    f"{column}コードがエイリアスマスタに存在しません"
                )
            
def validate_route_alias(df: pd.DataFrame, route_alias_dict: dict[tuple[str, str, str], str], errors: List) -> None:
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

