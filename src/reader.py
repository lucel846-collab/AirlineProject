from pathlib import Path

import pandas as pd


def read_excel(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    return df