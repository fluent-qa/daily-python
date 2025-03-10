import logging
from typing import List

import pandas as pd

from primary.pd_ext import ModelType


def models_to_file(items: List[ModelType], output_filename="", file_type="csv"):
    """
    Writes a list of Pydantic objects to an Excel/csv file.

    Args:
        items: A list of Pydantic model instances.
        output_filename: The name of the output Excel file (e.g., "output.xlsx").
        file_type: The type of output Excel file (e.g., "csv").
    """

    try:
        # Convert Pydantic objects to dictionaries
        data = [item.model_dump() for item in items]

        # Create a Pandas DataFrame
        df = pd.DataFrame(data)

        # Write the DataFrame to an Excel file
        if file_type == "csv":
            df.to_csv(output_filename, index=False)
        if file_type in ["xls", "xlsx"]:
            df.to_excel(output_filename, index=False, engine='openpyxl')  # Use openpyxl engine
        logging.info(f"Data successfully written to {output_filename}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
