def export_csv(df, path: Path) -> pd.DataFrame:
    df.to_csv(path, index=False, encoding="utf-8-sig")