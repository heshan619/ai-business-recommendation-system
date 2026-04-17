
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model(data: pd.DataFrame):
    """
    Train a simple linear regression model on daily sales data.

    Parameters:
        data: DataFrame with columns ['Order Date', 'Sales'].

    Returns:
        model: Trained LinearRegression model.
        processed_data: DataFrame with added numeric day index.
    """
    df = data.copy()

    # Ensure required columns exist
    if "Order Date" not in df.columns or "Sales" not in df.columns:
        raise ValueError("Data must contain 'Order Date' and 'Sales' columns.")

    # Convert dates and sort by date
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])
    df = df.sort_values("Order Date").reset_index(drop=True)

    # Use the number of days since the first order date as a numeric feature
    start_date = df["Order Date"].min()
    df["DayIndex"] = (df["Order Date"] - start_date).dt.days.astype(int)

    # Prepare training arrays
    X = df["DayIndex"].values.reshape(-1, 1)
    y = df["Sales"].astype(float).values

    model = LinearRegression()
    model.fit(X, y)

    return model, df


def predict_sales(model, data: pd.DataFrame, days: int = 7):
    """
    Predict future sales for the next N days.

    Parameters:
        model: Trained LinearRegression model.
        data: DataFrame used for training, with 'Order Date' column.
        days: Number of future days to predict.

    Returns:
        numpy.ndarray of predicted sales values.
    """
    if "Order Date" not in data.columns:
        raise ValueError("Data must contain 'Order Date' column.")

    df = data.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])

    last_date = df["Order Date"].max()
    start_date = df["Order Date"].min()

    # Create future day indices based on training start date
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days, freq="D")
    future_day_index = ((future_dates - start_date).days).astype(int).values.reshape(-1, 1)

    predictions = model.predict(future_day_index)
    return np.asarray(predictions)


def calculate_metrics(data: pd.DataFrame, predictions):
    """
    Calculate percentage change metrics for forecasted sales.

    Parameters:
        data: Historical DataFrame with 'Sales'.
        predictions: Array-like predicted sales values.

    Returns:
        Dictionary with percentage change metrics.
    """
    if "Sales" not in data.columns:
        raise ValueError("Data must contain 'Sales' column.")

    actual_sales = np.asarray(data["Sales"].astype(float))
    future_sales = np.asarray(predictions)

    if actual_sales.size == 0 or future_sales.size == 0:
        raise ValueError("Historical data and predictions must not be empty.")

    last_actual = actual_sales[-1]
    avg_actual = actual_sales.mean()
    peak_actual = actual_sales.max()
    last_prediction = future_sales[-1]

    def pct_change(new_value, reference):
        if reference == 0:
            return np.nan
        return ((new_value - reference) / reference) * 100

    return {
        "percent_change_vs_last_day": pct_change(last_prediction, last_actual),
        "percent_change_vs_average": pct_change(last_prediction, avg_actual),
        "percent_change_vs_peak": pct_change(last_prediction, peak_actual),
    }
