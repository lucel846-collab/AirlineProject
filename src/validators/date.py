from datetime import date, datetime

import pandas as pd

from src.validators.validator_result import ValidationResult


def validate_date_attr_check_daytype(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index,row in df.iterrows():
        if not isinstance(row["運航日"],(datetime,date)):
            result.add_error(
                filenm=filename,
                index=index,
                column="運航日",
                value=row["運航日"],
                message="運航日は日付形式である必要があります。"
            )

def validate_date_attr_check_monthtype(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    for index,row in df.iterrows():
        if not isinstance(row["年月"],(datetime,date)):
            result.add_error(
                filenm=filename,
                index=index,
                column="年月",
                value=row["年月"],
                message="年月は日付形式である必要があります。"
            )
def privious_month_first_day(df: pd.DataFrame)-> datetime:
    today = pd.Timestamp.today().normalize()
    first_date = today.replace(day=1)
    last_date_prev_month = first_date - pd.Timedelta(days=1)
    return last_date_prev_month.replace(day=1)
    
def privious_month_last_day(df: pd.DataFrame)-> datetime:
    today = pd.Timestamp.today().normalize()
    first_date = today.replace(day=1)
    return first_date - pd.Timedelta(days=1)
    

def validate_previous_date_check_daytype(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    last_date_prev_month = privious_month_last_day(df)
    first_date_prev_month = privious_month_first_day(df)
    for index,row in df.iterrows():
        if not (row["運航日"] <= last_date_prev_month and  row["運航日"] >= first_date_prev_month):
            result.add_error(
                filenm=filename,
                index=index,
                column="運航日",
                value=row["運航日"],
                message="運航日は前月である必要があります。"
        )

def validate_previous_date_check_monthtype(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    filename = df.attrs.get("filename")
    first_date_prev_month = privious_month_first_day(df)
    for index,row in df.iterrows():
        if ( row["年月"] != first_date_prev_month):
            result.add_error(
                filenm=filename,
                index=index,
                column="年月",
                value=row["年月"],
                message="年月は前月月初日である必要があります。"
        )
