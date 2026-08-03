import pandas as pd
from src.validators.adderror import add_error

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

def validate_columns(df: pd.DataFrame, errors: list[dict[str, any]]) -> None:

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append({"行番号":"","項目名":col,"入力値":"","エラー内容":"列が存在しません"})
 
def validate_required(df: pd.Dataframe, errors:list[dict[str, any]]) -> None:

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
