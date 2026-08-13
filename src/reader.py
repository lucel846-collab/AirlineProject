import os
from pathlib import Path

import pandas as pd


def read_excel(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    df.attrs["filename"] =  os.path.basename(path)
    return df