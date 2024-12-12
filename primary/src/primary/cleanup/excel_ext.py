import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Union, Tuple


def is_table_row(row: pd.Series) -> bool:
    """
    Check if a row is likely part of a table based on its content.
    
    Args:
        row: Pandas Series representing a row
        
    Returns:
        bool: True if the row appears to be part of a table
    """
    # Count non-null values
    non_null_count = row.notna().sum()
    
    # If most cells are filled, it's likely a table row
    if non_null_count > 2:
        return True
    
    return False


def find_table_boundaries(df: pd.DataFrame) -> List[Tuple[int, int]]:
    """
    Find the start and end rows of tables in the DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of tuples containing (start_row, end_row) for each table
    """
    table_boundaries = []
    in_table = False
    start_row = None
    min_rows = 3  # Minimum rows to consider as a table
    
    for idx, row in df.iterrows():
        is_table = is_table_row(row)
        
        if is_table and not in_table:
            # Start of a new table
            start_row = idx
            in_table = True
        elif not is_table and in_table:
            # End of current table
            if idx - start_row >= min_rows:
                table_boundaries.append((start_row, idx - 1))
            in_table = False
            start_row = None
    
    # Handle case where table extends to the end of file
    if in_table and (len(df) - start_row >= min_rows):
        table_boundaries.append((start_row, len(df) - 1))
    
    return table_boundaries


def clean_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and format the extracted table.
    
    Args:
        df: DataFrame to clean
        
    Returns:
        Cleaned DataFrame
    """
    # Remove completely empty rows and columns
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # If first row contains mostly non-null values, use it as header
    if df.iloc[0].notna().mean() > 0.5:
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Convert column names to string
    df.columns = df.columns.astype(str)
    
    return df


def extract_tables(excel_path: Union[str, Path], 
                  sheet_name: Union[str, int] = 0,
                  min_rows: int = 3,
                  min_cols: int = 2) -> List[pd.DataFrame]:
    """
    Extract tables from an Excel file that contains mixed content.
    
    Args:
        excel_path: Path to the Excel file
        sheet_name: Name or index of the sheet to process (default: 0)
        min_rows: Minimum number of rows to consider as a table (default: 3)
        min_cols: Minimum number of columns to consider as a table (default: 2)
        
    Returns:
        List of DataFrames, each containing an extracted table
    """
    # Read the Excel file
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    # Find table boundaries
    boundaries = find_table_boundaries(df)
    
    # Extract and clean tables
    tables = []
    for start, end in boundaries:
        table = df.iloc[start:end+1].copy()
        table = clean_table(table)
        
        # Only keep tables that meet minimum size requirements
        if len(table) >= min_rows and len(table.columns) >= min_cols:
            tables.append(table)
    
    return tables


def extract_project_details(excel_path: Union[str, Path], 
                          sheet_name: Union[str, int] = 0) -> pd.DataFrame:
    """
    Extract project details table from a credit rating report Excel file.
    
    Args:
        excel_path: Path to the Excel file
        sheet_name: Name or index of the sheet to process (default: 0)
        
    Returns:
        DataFrame containing the project details table
    """
    # Extract all tables
    tables = extract_tables(excel_path, sheet_name)
    
    # Look for the project details table
    # Usually it's the largest table with specific keywords in headers
    project_table = None
    max_size = 0
    
    for table in tables:
        # Convert headers to string and combine them
        headers = ' '.join(str(col) for col in table.columns)
        
        # Check if this looks like a project table
        keywords = ['项目', '金额', '期限', '规模']
        if any(keyword in headers for keyword in keywords):
            size = len(table) * len(table.columns)
            if size > max_size:
                max_size = size
                project_table = table
    
    if project_table is None:
        raise ValueError("Could not find project details table in the Excel file")
    
    return project_table
