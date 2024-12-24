from pathlib import Path

from loc_gov_bonds.test_standard_process import REWORKSPACE
from primary.cleanup import excel_ext


def test_extract_project_details():
    """
    Test extracting project details from credit rating report Excel file
    """
    excel_file = Path(REWORKSPACE) / "guangdong/2024/all_files/6. 2024年广东省政府专项债券（七十二期）信用评级报告.xlsx"
    
    # Extract all tables first
    print("\nExtracting all tables from Excel file:")
    tables = excel_ext.extract_tables(excel_file)
    print(f"Found {len(tables)} tables")
    
    # Print info about each table
    for i, table in enumerate(tables, 1):
        print(f"\nTable {i}:")
        print(f"Shape: {table.shape}")
        print("Columns:", list(table.columns))
        print("\nFirst few rows:")
        print(table.head(2))
        print("-" * 80)
    
    # Try to extract project details specifically
    print("\nExtracting project details table:")
    project_table = excel_ext.extract_project_details(excel_file)
    print("\nProject Details Table:")
    print(f"Shape: {project_table.shape}")
    print("Columns:", list(project_table.columns))
    print("\nFirst few rows:")
    print(project_table.head())
