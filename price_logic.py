import pandas as pd
import numpy as np
import os

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "processed",
    "cleaned_prices.csv"
)

def load_data():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")
    
    df = pd.read_csv(CSV_PATH)
    
    # Validate required columns
    required_cols = ["crop", "market", "price"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["trust_score"] = pd.to_numeric(df["trust_score"], errors="coerce").fillna(0.8)
    return df.dropna(subset=["price", "crop", "market"])

def get_price_range(crop, market):
    df = load_data()
    filtered = df[
        (df["crop"].str.lower() == crop) &
        (df["market"].str.lower() == market)
    ]

    if filtered.empty:
        return None

    weights = filtered["trust_score"].clip(lower=0.01)
    avg_price = int(round(np.average(filtered["price"], weights=weights)))
    min_price = int(filtered["price"].min())
    max_price = int(filtered["price"].max())

    return [{
        "crop": crop,
        "market": market,
        "price": avg_price,
        "min": min_price,
        "max": max_price,
        "unit": "quintal"
    }]
