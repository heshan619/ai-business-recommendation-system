
import os
from typing import Union

import pandas as pd


def load_data(file):
    """
    Load data from a CSV or Excel file into a pandas DataFrame.

    Parameters:
        file: Path to the input file or file-like object.

    Returns:
        pandas.DataFrame with loaded data.
    """
    if isinstance(file, (str, os.PathLike)):
        extension = os.path.splitext(str(file))[1].lower()
        if extension in {".csv"}:
            return pd.read_csv(file)
        elif extension in {".xls", ".xlsx"}:
            return pd.read_excel(file)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")
    else:
        # Fallback for file-like objects: try CSV first, then Excel
        try:
            return pd.read_csv(file)
        except Exception:
            file.seek(0)
            return pd.read_excel(file)


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and aggregate sales data by date.

    Steps:
        - Convert 'Order Date' column to datetime.
        - Drop rows with missing order dates.
        - Fill missing sales values with 0.
        - Aggregate daily sales.

    Parameters:
        df: Raw sales DataFrame.

    Returns:
        Cleaned DataFrame with columns ['Order Date', 'Sales'].
    """
    df = df.copy()

    if "Order Date" not in df.columns:
        raise ValueError("Missing required column: 'Order Date'")

    # Convert Order Date to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    # Drop rows with invalid or missing dates
    df = df.dropna(subset=["Order Date"])

    # Ensure Sales column exists and fill missing values
    if "Sales" not in df.columns:
        raise ValueError("Missing required column: 'Sales'")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0.0)

    # Normalize date first
    df["Order Date"] = df["Order Date"].dt.normalize()

    # Aggregate sales by date
    daily_sales = (
    df.groupby("Order Date", as_index=False)["Sales"]
    .sum())
    return daily_sales

def validate_data(df: pd.DataFrame) -> None:
    """
    Validate that the DataFrame contains required columns.

    Parameters:
        df: DataFrame to validate.

    Raises:
        ValueError if required columns are missing.
    """
    required_columns = {"Order Date", "Sales"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {', '.join(sorted(missing))}")
