import pandas as pd
import os
from market_cap_export import download_market_cap_history  # Import only the function

# Define the path to the Excel file
file_path = "data/holdings-daily-us-en-spy.xlsx"

# Load the Excel file and list available sheets
try:
    xls = pd.ExcelFile(file_path)
    print(f"Available sheets: {xls.sheet_names}")  # Debugging: Print sheet names

    # Load the first sheet, skipping the first 4 row (since headers are misaligned)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], skiprows=4)

    # Rename columns to expected names
    df.columns = ["Name", "Ticker", "Identifier", "SEDOL", "Weight", "Sector", "Shares Held", "Local Currency"]

    print(df.head())  # Debugging: Show first few rows

except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Ensure 'Ticker' column exists
expected_ticker_col = "Ticker"
if expected_ticker_col not in df.columns:
    print(f"Error: Expected column '{expected_ticker_col}' not found. Available columns: {df.columns}")
    exit()

# Extract tickers, removing NaN values
tickers = df[expected_ticker_col].dropna().astype(str).tolist()

# Create a directory to store the output if it doesn’t exist
output_dir = "companies_market_cap_data"
os.makedirs(output_dir, exist_ok=True)

# Loop through each ticker and fetch market cap history
for ticker in tickers:
    print(f"Processing market cap history for {ticker}...")
    try:
        download_market_cap_history(ticker)
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

print("All tickers processed successfully.")

