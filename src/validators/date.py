import pandas as pd
from src.detect_layout import detect_layout
from src.validator_result import ValidationResult


def validate_previous_date_check(df: pd.DataFrame, result: ValidationResult) -> None:
    today = pd.Timestamp.today().normalize()
    first_date = today.replace(day=1)
    last_date_prev_month = first_date - pd.Timedelta(days=1)
    first_date_prev_month = last_date_prev_month.replace(day=1)
    layout = detect_layout(df)
    if layout == "DAILY_FLIGHT":

        for index,row in df.iterrows():
            if (row["運航日"] > last_date_prev_month or row["運航日"] < first_date_prev_month):
                result.add_error(
                    index=index,
                    column="運航日",
                    value=row["運航日"],
                    message="運航日は前月である必要があります。"
            )
    elif layout == "MONTHLY_ROURTE":
        for index,row in df.iterrows():
            if ( row["年月"] != first_date_prev_month):
                result.add_error(
                    index=index,
                    column="年月",
                    value=row["年月"],
                    message="年月は前月月初日である必要があります。"
            )
