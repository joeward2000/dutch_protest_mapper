# src/data_clean.py
import os
import pandas as pd
import numpy as np
from data_load import load_raw_data, clean_column_names

DATA_PATH = "./data/processed/protests_nl_cleaned.csv"

def clean_data(df):
    """
    Keep selected columns, filter for geo_precision=1 and time_precision=1,
    relabel excessive force events, drop precision columns and rename columns.
    """
    # Columns to retain
    keep_cols = [
        "year",
        "time_precision",
        "sub_event_type",
        "interaction",
        "admin1",
        "location",
        "geo_precision",
        "source",
        "notes",
        "tags",
        "longitude",
        "latitude"
    ]
    df = df[keep_cols]

    # Filter for exact date and location
    df = df[(df["geo_precision"] == 1) & (df["time_precision"] == 1)]

    # Relabel excessive force events
    df["sub_event_type"] = df["sub_event_type"].replace(
        "Excessive force against protesters", "Protest with intervention"
    )

    # Drop precision columns
    df = df.drop(columns=["geo_precision", "time_precision"])

    # Rename columns
    df = df.rename(columns={
        "admin1": "province",
        "sub_event_type": "event_type"
    })

    return df

def save_data(df, path=DATA_PATH):
    """Save cleaned dataset."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned data saved to {path}")

if __name__ == "__main__":
    # Load and clean
    df = load_raw_data()
    df = clean_column_names(df)
    df = clean_data(df)

    # Save
    save_data(df)

    # Quick check
    print(f"Rows after cleaning: {len(df)}")
    print("Preview of cleaned dataset:")
    print(df.head())