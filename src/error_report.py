from pathlib import Path

import pandas as pd


def export_validation_errors(errors, path: Path):

    df = pd.DataFrame(errors)

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
    )