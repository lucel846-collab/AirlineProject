from dataclasses import dataclass

import pandas as pd


@dataclass
class ReadResult:
    df:pd.DataFrame
    layout: str
