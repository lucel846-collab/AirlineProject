from pathlib import Path

import pandas as pd


def read_excel(path:Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    df["運航日"] = pd.to_datetime(df["運航日"])
    return df