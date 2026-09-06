from datetime import date, datetime, time, timedelta

import pandas as pd

from src.validators.validator_result import ValidationResult


def validate_check_time_range(df: pd.DataFrame,_master, result: ValidationResult) -> None:
    ffilename = df.attrs.get("filename")
    for column in ("出発時刻", "到着時刻"):
        for index, value in df[column].items():
            if value is None or value== "" :
                 continue  # Skip validation for null values
            value = int(float(value))
            if not (0 <= value <= 2359):
                result.add_error(
                    filenm=ffilename,
                    index=index,
                    column=column,
                    value=value,
                    message="時刻数字ではないです"
                )
                continue

            hour = value // 100  # 時間を取得
            minute = value % 100   # 分を取得
            
            # 時間が0〜23、分が0〜59の範囲かチェック
            if 0 <= hour <= 23 and 0 <= minute <= 59 :
                pass
            else:            
                result.add_error(
                    filenm=ffilename,
                    index=index,
                    column=column,
                    value=value,
                    message="時刻範囲ではないです"
                )

def convert_to_datetime(target_date: date, time_num: int) -> datetime:
   
    hour = time_num // 100
    minute = time_num % 100
    
    t = time(hour, minute)
    return datetime.combine(target_date, t)

def convert_to_datetime_minus(target_date: date, time_num: int) -> datetime:
    # 前段で日時型になっている出発時刻から、リードタイム（分）を引き算する
    return target_date - timedelta(minutes=time_num)