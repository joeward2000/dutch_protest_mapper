# src/data_clean.py

import os
import pandas as pd
from data_load import load_raw_data, clean_column_names

INTERIM_DATA_PATH = "data/interim/protests_nl_cleaned.csv"

def clean_data(df):
    """
    Keep selected columns, filter for geo_precision=1 and time_precision=1,
    drop these columns afterwards, and rename admin1 to province.
    """
    # Columns to retain
    keep_cols = [
        "event_date",
        "time_precision",
        "sub_event_type",
        "interaction",
        "admin1",
        "geo_precision",
        "source",
        "notes",
        "tags",
    ]
    df = df[keep_cols]

    # Filter for exact date and location
    df = df[(df["geo_precision"] == 1) & (df["time_precision"] == 1)]

    # Drop precision columns
    df = df.drop(columns=["geo_precision", "time_precision"])

    # Rename admin1 -> province
    df = df.rename(columns={"admin1": "province"})

    return df

def save_interim_data(df, path=INTERIM_DATA_PATH):
    """Save cleaned-but-not-final dataset."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Interim cleaned data saved to {path}")

if __name__ == "__main__":
    # Load and clean
    df = load_raw_data()
    df = clean_column_names(df)
    df = clean_data(df)

    # Save
    save_interim_data(df)

    # Quick check
    print(f"Rows after cleaning: {len(df)}")
    print("Preview of cleaned dataset:")
    print(df.head())
