from pathlib import Path
from typing import Iterable

import pandas as pd


def remove_duplicates(
    dataframe: pd.DataFrame,
    key_columns: Iterable[str],
) -> pd.DataFrame:
    return dataframe.drop_duplicates(subset=list(key_columns), keep="last")


def validate_not_null(
    dataframe: pd.DataFrame,
    required_columns: Iterable[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    required_columns = list(required_columns)

    invalid_mask = dataframe[required_columns].isnull().any(axis=1)

    valid_records = dataframe.loc[~invalid_mask].copy()
    rejected_records = dataframe.loc[invalid_mask].copy()

    if not rejected_records.empty:
        rejected_records["_rejection_reason"] = (
            "Required column contains null value"
        )

    return valid_records, rejected_records


def save_rejected_records(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    if not dataframe.empty:
        dataframe.to_parquet(output_path, index=False)