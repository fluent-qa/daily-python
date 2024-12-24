from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import pandas as pd
from .convert_funcs import read_to_df



def filter_by_columns(df: pd.DataFrame, column_filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Generic function to filter DataFrame based on column filters

    Args:
        df: Source DataFrame
        column_filters: Dict where key is column name and value is filter value
            Example: {"年份": 2024, "地区名称": "广东省"}

    Returns:
        Filtered DataFrame
    """
    try:
        # Validate all columns exist
        missing_cols = [col for col in column_filters.keys() if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns in DataFrame: {missing_cols}")

        # Build filter condition
        mask = pd.Series(True, index=df.index)
        for column, value in column_filters.items():
            mask &= (df[column] == value)

        return df[mask]

    except Exception as e:
        print(f"Error filtering DataFrame: {str(e)}")
        raise


def filter_table_file(excel_file: str | Path, column_filters: Dict[str, Any], output_path: str, file_type="csv"):
    df = read_to_df(excel_file, file_type)
    filtered_df = filter_by_columns(df, column_filters)
    filtered_df.to_csv(output_path, index=False)
