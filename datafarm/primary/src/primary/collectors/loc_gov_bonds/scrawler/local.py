import os
import re

import pandas as pd
import logging
import json

# Configure logging
logging.basicConfig(
    filename='file_processing.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def process_data_files(data_folder_path, output_excel_path):
    """
    Read all numbered JSON files from data folder and combine them into an Excel file.
    Only extracts the 'data' field from each JSON file.
    """
    all_data = []

    # Get all files in the data folder, excluding xlsx files
    files = [f for f in os.listdir(data_folder_path) if not f.endswith('.xlsx')]

    # Define Chinese column headers based on your JSON structure
    chinese_headers = {
        'source_file': '文件名',
        'AD_CODE_GK': '行政区划代码',
        'SET_YEAR_GK': '年份',
        'AD_NAME': '地区名称',
        'ZQ_NAME': '债券名称',
        'ZQ_CODE': '债券代码',
        'ZQ_JC': '债券简称',
        'ZQQX_NAME': '债券期限',
        'FX_AMT': '发行金额',
        'XZZQ_AMT': '新增债券金额',
        'ZHZQ_AMT': '置换债券金额',
        'ZRZZQ_AMT': '再融资债券金额',
        'QX_DATE': '起息日期',
        'ZQLX_NAME': '债券类型',
        'LL': '利率',
        'ZQ_FXTIME': '发行日期',
        'FXFS': '付息方式'
    }

    # Process each file
    for file_name in files:
        file_path = os.path.join(data_folder_path, file_name)

        try:
            # Read JSON content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if file is empty
            if not content.strip():
                logging.error(f"Empty file found: {file_path}")
                continue

            # Parse JSON and extract data field
            json_data = json.loads(content)
            if 'data' not in json_data:
                logging.error(f"No 'data' field in file: {file_path}")
                continue

            # Convert to DataFrame
            df = pd.DataFrame(json_data['data'])

            # Add file name column
            df['source_file'] = file_name

            all_data.append(df)

        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")
            continue

    if all_data:
        # Combine all DataFrames
        combined_df = pd.concat(all_data, ignore_index=True)

        # Reorder columns to put source_file first
        columns_to_keep = ['source_file'] + [col for col in chinese_headers.keys() if col != 'source_file']
        combined_df = combined_df[columns_to_keep]

        # Rename columns to Chinese
        combined_df = combined_df.rename(columns=chinese_headers)

        # Export to Excel
        combined_df.to_excel(output_excel_path, index=False)
        print(f"Data successfully exported to {output_excel_path}")
    else:
        print("No valid data found to export")


def extract_file_numbers():
    # Read the log file
    with open('file_processing.log', 'r') as f:
        content = f.read()

    # Use regex to extract file numbers
    # Pattern matches numbers between 'data/' and the end of path
    pattern = r'data/(\d+)'
    file_numbers = re.findall(pattern, content)

    # Convert to set to remove duplicates and sort
    unique_numbers = sorted(set(file_numbers), key=int)

    # Print results
    print(f"Total unique files: {len(unique_numbers)}")
    print("File numbers:")
    print(unique_numbers)

    # Optionally save to a text file
    with open('file_numbers.txt', 'w') as f:
        f.write('\n'.join(unique_numbers))

    return unique_numbers



