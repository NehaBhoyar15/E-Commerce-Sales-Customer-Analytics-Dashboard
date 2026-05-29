"""
========================================================
  E-Commerce Sales & Customer Analytics Dashboard
  Script 1: Data Cleaning & Preprocessing
  Author  : Data Analyst Intern
  Dataset : Superstore Sales Dataset
========================================================
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. LOAD DATASET
# ─────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    """Load the Superstore CSV dataset."""
    df = pd.read_csv(filepath, encoding="latin-1")
    print(f"✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


# ─────────────────────────────────────────────
# 2. INITIAL INSPECTION
# ─────────────────────────────────────────────
def initial_inspection(df: pd.DataFrame) -> None:
    """Print a quick overview of the raw dataset."""
    print("\n── Shape ──────────────────────────────────────")
    print(df.shape)

    print("\n── Column Data Types ──────────────────────────")
    print(df.dtypes)

    print("\n── First 5 Rows ────────────────────────────────")
    print(df.head())

    print("\n── Missing Values ──────────────────────────────")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values found.")

    print("\n── Duplicate Rows ──────────────────────────────")
    print(f"Duplicates: {df.duplicated().sum()}")

    print("\n── Basic Statistics ────────────────────────────")
    print(df.describe())


# ─────────────────────────────────────────────
# 3. HANDLE MISSING VALUES
# ─────────────────────────────────────────────
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Impute or drop missing values per column type."""

    # Numeric columns → fill with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"  [Numeric]  '{col}' → filled with median ({median_val:.2f})")

    # Categorical / object columns → fill with mode
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"  [Categorical] '{col}' → filled with mode ('{mode_val}')")

    print(f"\n✅ Missing values handled. Remaining: {df.isnull().sum().sum()}")
    return df


# ─────────────────────────────────────────────
# 4. REMOVE DUPLICATES
# ─────────────────────────────────────────────
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate rows."""
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    print(f"✅ Duplicates removed: {before - after} rows dropped ({after} remaining)")
    return df


# ─────────────────────────────────────────────
# 5. FORMAT DATES
# ─────────────────────────────────────────────
def format_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date strings to datetime objects."""
    date_columns = ["Order Date", "Ship Date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
            print(f"  ✅ '{col}' → datetime64")

    # Drop rows where dates couldn't be parsed
    invalid_dates = df[date_columns].isnull().any(axis=1).sum()
    if invalid_dates:
        df.dropna(subset=date_columns, inplace=True)
        print(f"  ⚠️  {invalid_dates} rows with unparseable dates removed.")

    return df


# ─────────────────────────────────────────────
# 6. DATA TYPE CONVERSION
# ─────────────────────────────────────────────
def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Enforce correct dtypes for key columns."""
    type_map = {
        "Sales":    float,
        "Profit":   float,
        "Quantity": int,
        "Discount": float,
    }
    for col, dtype in type_map.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(dtype)
            print(f"  ✅ '{col}' → {dtype.__name__}")

    # Standardise string columns (strip whitespace, title-case)
    str_cols = ["Customer Name", "Region", "Category", "Sub-Category",
                "Product Name", "Ship Mode", "Segment", "State", "City"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    print("✅ Data types converted.")
    return df


# ─────────────────────────────────────────────
# 7. FEATURE ENGINEERING
# ─────────────────────────────────────────────
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived / business-logic columns."""

    # ── Time features ──────────────────────────
    df["Order Year"]        = df["Order Date"].dt.year
    df["Order Month"]       = df["Order Date"].dt.month
    df["Order Month Name"]  = df["Order Date"].dt.strftime("%b")
    df["Order Quarter"]     = df["Order Date"].dt.quarter
    df["Order Day of Week"]  = df["Order Date"].dt.day_name()

    # ── Shipping lead time ─────────────────────
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # ── Profitability ratio ────────────────────
    df["Profit Margin (%)"] = np.where(
        df["Sales"] != 0,
        (df["Profit"] / df["Sales"]) * 100,
        0
    ).round(2)

    # ── Revenue per unit ─────────────────────
    df["Revenue per Unit"] = np.where(
        df["Quantity"] != 0,
        df["Sales"] / df["Quantity"],
        0
    ).round(2)

    # ── Profit flag ───────────────────────────
    df["Is Profitable"] = df["Profit"].apply(lambda x: "Profitable" if x > 0 else "Loss")

    # ── Sales buckets ─────────────────────────
    df["Sales Bucket"] = pd.cut(
        df["Sales"],
        bins=[0, 100, 500, 1000, 5000, np.inf],
        labels=["< $100", "$100–$500", "$500–$1K", "$1K–$5K", "$5K+"]
    )

    # ── Customer order number ─────────────────
    df.sort_values(["Customer Name", "Order Date"], inplace=True)
    df["Customer Order #"] = df.groupby("Customer Name").cumcount() + 1

    # ── Repeat customer flag ──────────────────
    order_counts = df.groupby("Customer Name")["Order ID"].nunique()
    df["Is Repeat Customer"] = df["Customer Name"].map(
        lambda name: "Repeat" if order_counts.get(name, 0) > 1 else "New"
    )

    print(f"✅ Feature engineering done. New columns: Order Year, Order Month, "
          f"Order Quarter, Shipping Days, Profit Margin (%), Revenue per Unit, "
          f"Is Profitable, Sales Bucket, Customer Order #, Is Repeat Customer")
    return df


# ─────────────────────────────────────────────
# 8. OUTLIER DETECTION (IQR)
# ─────────────────────────────────────────────
def detect_outliers(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Flag outliers using the IQR method (does NOT drop them)."""
    for col in columns:
        if col in df.columns:
            Q1  = df[col].quantile(0.25)
            Q3  = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            n_out = ((df[col] < lower) | (df[col] > upper)).sum()
            flag_col = f"{col}_Outlier"
            df[flag_col] = ((df[col] < lower) | (df[col] > upper))
            print(f"  📊 '{col}': {n_out} outliers flagged (lower={lower:.2f}, upper={upper:.2f})")
    return df


# ─────────────────────────────────────────────
# 9. SAVE CLEAN DATA
# ─────────────────────────────────────────────
def save_clean_data(df: pd.DataFrame, output_path: str) -> None:
    """Export the cleaned DataFrame to CSV."""
    df.to_csv(output_path, index=False)
    print(f"\n✅ Clean dataset saved → {output_path}")
    print(f"   Final shape: {df.shape[0]} rows × {df.shape[1]} columns")


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def run_cleaning_pipeline(raw_path: str, clean_path: str) -> pd.DataFrame:
    print("=" * 60)
    print("  DATA CLEANING PIPELINE — E-Commerce Analytics")
    print("=" * 60)

    df = load_data(raw_path)

    print("\n[STEP 1] Initial Inspection")
    initial_inspection(df)

    print("\n[STEP 2] Handling Missing Values")
    df = handle_missing_values(df)

    print("\n[STEP 3] Removing Duplicates")
    df = remove_duplicates(df)

    print("\n[STEP 4] Formatting Dates")
    df = format_dates(df)

    print("\n[STEP 5] Converting Data Types")
    df = convert_data_types(df)

    print("\n[STEP 6] Feature Engineering")
    df = feature_engineering(df)

    print("\n[STEP 7] Outlier Detection")
    df = detect_outliers(df, ["Sales", "Profit", "Quantity", "Discount"])

    print("\n[STEP 8] Saving Clean Data")
    save_clean_data(df, clean_path)

    print("\n" + "=" * 60)
    print("  ✅ PIPELINE COMPLETE")
    print("=" * 60)
    return df


# ─────────────────────────────────────────────
if __name__ == "__main__":
    RAW_PATH   = "../data/superstore_raw.csv"
    CLEAN_PATH = "../data/superstore_clean.csv"
    df_clean = run_cleaning_pipeline(RAW_PATH, CLEAN_PATH)
