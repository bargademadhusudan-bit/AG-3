import pandas as pd
import os
import sys

# Ensure console uses UTF-8 on Windows to avoid UnicodeEncodeError for emojis
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Get the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)

# 1. Load raw data
raw_path = os.path.join(project_root, "data", "raw", "mandi_prices.csv")
if not os.path.exists(raw_path):
    raise FileNotFoundError(raw_path)

df = pd.read_csv(raw_path)

print(f"✅ Loaded {len(df)} rows from {raw_path}")

# 2. Drop missing values
df = df.dropna()
print(f"✅ After removing NaN: {len(df)} rows")

# 3. Filter by trust score
df = df[df["trust_score"] >= 0.5]
print(f"✅ After trust_score filter: {len(df)} rows")

# 4. Filter by distance (nearby markets only)
df = df[df["distance_km"] <= 25]
print(f"✅ After distance filter: {len(df)} rows")

# 5. Keep only one unit (quintal)
df = df[df["unit"] == "quintal"]
print(f"✅ After unit filter: {len(df)} rows")

# 6. Remove price outliers using IQR (group-wise)
def remove_outliers(group):
    if len(group) < 2:
        return group
    q1 = group["price"].quantile(0.25)
    q3 = group["price"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return group[(group["price"] >= lower) & (group["price"] <= upper)]

df = df.groupby(["crop", "market"]).apply(remove_outliers)
df = df.reset_index(drop=True)
print(f"✅ After outlier removal: {len(df)} rows")

# 7. Sort data
df = df.sort_values(by=["date", "crop", "market"])

# 8. Create processed directory if it doesn't exist
processed_dir = os.path.join(project_root, "data", "processed")
os.makedirs(processed_dir, exist_ok=True)

# 9. Save cleaned data
processed_path = os.path.join(processed_dir, "cleaned_prices.csv")
df.to_csv(processed_path, index=False)

print(f"✅ Data cleaned and saved to {processed_path}")
print(f"✅ Final dataset: {len(df)} rows, {len(df.columns)} columns")