from __future__ import annotations

import csv
import re
from pathlib import Path


def first_cell_empty_handler(row):
    return len(row[0].strip()) == 0


def clean_data(row):
    # 去除空值
    cleaned_row = [cell for cell in row if cell]
    # 处理包含回车符号和逗号的字符串
    cleaned_row = [re.sub(r'[\n,]', '', cell) for cell in cleaned_row]
    cleaned_row = [re.sub(r'[\s+,]', '', cell) for cell in cleaned_row]
    return cleaned_row


def clean_csv_empty_column(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
            open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = clean_data(row)
            writer.writerow(cleaned_row)


def clean_csv_rows(input_file: str | Path, output_file: str | Path, row_handlers=None):
    """
    Clean a CSV file by filtering out rows based on custom handlers.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output CSV file
        row_handlers (list[callable], optional): List of functions to filter rows.
            Each function takes a row as input and returns a boolean indicating
            whether the row should be kept or not.
    """
    if row_handlers is None:
        row_handlers = [first_cell_empty_handler]
    if row_handlers is None:
        row_handlers = []

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
            open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        loop_index = 0
        for row in reader:
            cleaned_row = clean_data(row)
            if loop_index > 0:
                if any(handler(cleaned_row) for handler in row_handlers):
                    continue
            loop_index += 1
            writer.writerow(cleaned_row)


def replace_dots_except_last(text):
    """
    Replace all dots in a string except the last one.
    
    Args:
        text (str): Input text containing dots
        
    Returns:
        str: Text with all dots replaced except the last one
    
    Example:
        >>> replace_dots_except_last("1.2.3.4")
        "123.4"
    """
    if not isinstance(text, str):
        return text

    # Count the number of dots
    dot_count = text.count('.')
    if dot_count <= 1:
        return text

    # Find the last dot
    last_dot_index = text.rindex('.')

    # Replace all dots before the last one
    first_part = text[:last_dot_index].replace('.', '')
    last_part = text[last_dot_index:]

    return first_part + last_part
