from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, List, Type

import pandas as pd
import rich

from .models import ModelType


def read_to_df(file_path: str | Path, file_type: str = "csv", use_cols=None) -> pd.DataFrame:
    # Read file
    if file_type == "xlsx":
        df = pd.read_excel(file_path, dtype=str, na_filter=False, usecols=use_cols)
    elif file_type == "csv":
        df = pd.read_csv(file_path, dtype=str, na_filter=False, usecols=use_cols, encoding="utf-8")
    else:
        raise ValueError("file_type must be either 'xlsx' or 'csv'")
    new_df = df.drop_duplicates()
    return new_df


def clean_text_columns(df: pd.DataFrame,
                       columns: list = None,
                       replace_with: str = '') -> pd.DataFrame:
    """
    清理指定列或所有文本列中的换行符和多余空格

    Parameters:
        df: 输入的DataFrame
        columns: 要处理的列名列表，默认处理所有文本列
        replace_with: 用于替换换行符的字符，默认为空格
    """
    df = df.copy()

    # 如果没有指定列，则处理所有文本列
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns

    for col in columns:
        if col in df.columns:
            # 1. 替换换行符
            df[col] = df[col].astype(str).replace('\n', replace_with, regex=True)

            # 2. 替换回车符
            df[col] = df[col].replace('\r', replace_with, regex=True)

            # 3. 替换多个连续空格为单个空格
            # df[col] = df[col].replace('\s+', ' ', regex=True)

            # 4. 去除首尾空格
            df[col] = df[col].str.strip()
            #
            # # 5. 将'nan'和'None'字符串转换回NaN
            # df[col] = df[col].replace({'nan': np.nan, 'None': np.nan})
    return df


def convert_df_by_alias(source_df: pd.DataFrame,
                        standard_columns: List[str],
                        field_mappings: Dict,
                        default_values: Optional[Dict] = None) -> pd.DataFrame:
    """Convert DataFrame columns using field mappings and standard column definitions.

    This function transforms a source DataFrame into a new DataFrame with standardized column names.
    It supports column aliasing through field mappings and can set default values for specified columns.

    Args:
        source_df (pd.DataFrame): The input DataFrame to be converted
        standard_columns (List[str]): List of standard column names for the output DataFrame
        field_mappings (Dict): Dictionary mapping source column names to destination column names
                              e.g., {'old_name': 'new_name', 'customer_id': 'id'}
        default_values (Optional[Dict], optional): Dictionary of default values for columns
                                                 e.g., {'status': 'active', 'region': 'NA'}

    Raises:
        ValueError: If standard_columns is empty

    Returns:
        pd.DataFrame: A new DataFrame with mapped columns and default values applied
    
    Example:
        >>> source_df = pd.DataFrame({'old_name': ['John', 'Alice'], 'age': [25, 30]})
        >>> standard_cols = ['name', 'age', 'status']
        >>> mappings = {'old_name': 'name'}
        >>> defaults = {'status': 'active'}
        >>> result = convert_df_by_alias(source_df, standard_cols, mappings, defaults)
    """
    if len(standard_columns) > 0:
        new_df = pd.DataFrame(columns=standard_columns)
    else:
        raise ValueError("please provider standard column names")

    if len(field_mappings) == 0:
        for standard_column in standard_columns:
            if standard_column in source_df.columns:
                new_df[standard_column] = source_df[standard_column]
    else:
        for src_col, dst_col in field_mappings.items():
            if dst_col and src_col in source_df.columns:
                new_df[dst_col] = source_df[src_col]

    if default_values is not None:
        for col, value in default_values.items():
            if col in standard_columns:
                new_df[col] = value
    return new_df


def read_to_models_by_field_mapping(df: pd.DataFrame, field_mappings: Dict, model_class: Type[ModelType]) -> \
        List[ModelType]:
    result = []
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        if field_mappings:
            mapped_row_dict = {}
            for key, value in field_mappings.items():
                if value:
                    mapped_row_dict[key] = row_dict.get(value, None)

            data = model_class(**mapped_row_dict)
            result.append(data)
    return result


def read_to_models(
        excel_path: str | Path,
        model_class: Type[ModelType],
        file_type: str = "csv"
) -> List[ModelType]:
    """
    Generic function to read Excel/CSV file and convert to Pydantic/SQLModel models

    Args:
        excel_path: Path to the Excel/CSV file
        model_class: The Pydantic/SQLModel class to convert to
        file_type: File type, either "xlsx" or "csv"

    Returns:
        List of model instances
    """
    try:
        # Get field aliases mapping
        field_aliases = {
            field.alias: field_name
            for field_name, field in model_class.model_fields.items()
            if field.alias
        }

        # Read file
        df = read_to_df(file_path=excel_path, file_type=file_type)
        df = df.drop_duplicates()
        # Rename columns if aliases exist
        if field_aliases:
            df = df.rename(columns=field_aliases)

        # Convert to model list
        models = []
        for index, row in df.iterrows():
            try:
                row_dict = row.where(pd.notna(row), None).to_dict()
                model = model_class(**row_dict)
                models.append(model)
            except Exception as e:
                rich.print(f"Row {index + 2} validation failed: {e}")
                continue

        return models
    except Exception as e:
        print(f"Error processing file: {e}")
        return []


def ffill_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    数据合并处理,ffill with colum names
    """
    # 创建DataFrame的副本以避免SettingWithCopyWarning
    df = df.copy()
    # 3. 删除Unnamed列前进行验证
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    print(f"将删除以下列: {unnamed_cols}")

    # 删除Unnamed列
    df = df.drop(columns=unnamed_cols)

    # 4. 最终验证
    rich.print("\n最终数据统计:")
    print(f"总行数: {len(df)}")
    print(f"列名: {df.columns.tolist()}")
    print("\n每列的NaN值数量:")
    print(df.isna().sum())

    return df


def merge_by_column_mappings(df: pd.DataFrame, column_mappings: List[str] = None) -> pd.DataFrame:
    """
    # 1. 处理债券名称列
    if '债券名称' in df.columns:
        # 使用前向填充，并指定限制范围（可选）
        df['债券名称'] = df['债券名称'].fillna(method='ffill', limit=None)

    if '债券期数' in df.columns:
        # 使用前向填充，并指定限制范围（可选）
        df['债券期数'] = df['债券期数'].fillna(method='ffill', limit=None)

    if '债券年限（年）' in df.columns:
        # 使用前向填充，并指定限制范围（可选）
        df['债券年限（年）'] = df['债券年限（年）'].fillna(method='ffill', limit=None)
        # 可以添加验证确保填充正确
        assert df['债券期数'].isna().sum() == 0, "债券名称列仍有NaN值"
    :param df:
    :param column_mappings:
    :return:
    """
    for col in column_mappings:
        if col in df.columns:
            df[col] = df[col].fillna(method='ffill', limit=None)

    return df


def merge_unnamed_columns(df: pd.DataFrame, col_names=None) -> pd.DataFrame:
    if col_names is None:
        col_names = ['项目名称']
    for col in col_names:
        if col in df.columns:
            # 获取所有Unnamed列，按列名排序以确保顺序
            unnamed_cols = sorted([col for col in df.columns if 'Unnamed' in col])

            for col in unnamed_cols:
                # 只在项目名称为NaN时使用Unnamed列的非NaN值填充
                mask = df[col].isna() & df[col].notna()
                df.loc[mask, col] = df.loc[mask, col]
                filled_count = mask.sum()
                if filled_count > 0:
                    print(f"使用 {col} 填充了 {filled_count} 个")
    return df


def clean_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrame by creating a new DataFrame with proper columns and values

    1. Create new DataFrame with clean headers (no unnamed columns)
    2. Copy values using the rule: if current cell is empty, get next non-empty cell value
    """
    # 1. Get clean headers (skip unnamed columns)
    clean_headers = [
        str(col).strip()
        for col in df.columns
        if 'Unnamed' not in str(col) and str(col).strip()
    ]

    # 2. Create new DataFrame with clean headers
    cleaned_df = pd.DataFrame(columns=clean_headers)

    # 3. Process each row
    for idx in range(len(df)):
        row = df.iloc[idx]
        new_row = {}
        current_clean_col = 0  # Index for clean headers

        # Process each column in original DataFrame
        for i in range(len(df.columns)):
            value = row.iloc[i]

            # Skip if we've filled all clean columns
            if current_clean_col >= len(clean_headers):
                break

            # If this is a named column or has value
            if (not pd.isna(value) and str(value).strip()) or \
                    ('Unnamed' not in str(df.columns[i])):

                # Add to new row if we haven't filled this column yet
                if clean_headers[current_clean_col] not in new_row:
                    new_row[clean_headers[current_clean_col]] = value
                    current_clean_col += 1

        # Add the processed row to cleaned DataFrame
        cleaned_df.loc[idx] = new_row

    return cleaned_df


def append_models_to_csv(models: List[ModelType], csv_path: str):
    # Read existing CSV headers
    try:
        existing_df = pd.read_csv(csv_path, nrows=0)
        existing_headers = existing_df.columns.tolist()
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file {csv_path} not found!")

    # Convert models to DataFrame
    data = [model.model_dump() for model in models]
    new_df = pd.DataFrame(data)

    # Ensure new data matches existing columns
    new_df = new_df.reindex(columns=existing_headers)

    # Append to CSV without headers
    new_df.to_csv(
        csv_path,
        mode='a',  # Append mode
        header=False,  # Don't write headers again
        index=False,
        encoding='utf-8-sig'
    )
