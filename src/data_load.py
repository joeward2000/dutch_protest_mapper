import os
import pandas as pd

# Determine the repo root (one level up from src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "protests_nl_2020_2024.csv")

def load_raw_data(path=RAW_DATA_PATH):
    """Load the raw ACLED CSV file."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw data file not found at {path}. Please download it from ACLED and place it there."
        )
    df = pd.read_csv(path)
    return df

def clean_column_names(df):
    """Convert column names to lowercase and replace spaces with underscores."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

if __name__ == "__main__":
    df = load_raw_data()
    df = clean_column_names(df)
    print("Data loaded successfully.")
    print(f"Number of rows: {len(df)}")
    print("Preview of columns:", df.columns.tolist())
    print(df.head())
