from pathlib import Path

import pandas as pd


def load_sales() -> pd.DataFrame:
    """Load the bundled synthetic sales data, with revenue in USD."""
    return pd.read_csv(
        Path(__file__).resolve().parent / "data" / "sales.csv",
        parse_dates=["date"],
        dtype={"region": "string", "product": "string", "quantity": "int64", "revenue": "float64"},
    )
