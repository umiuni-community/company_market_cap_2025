import pandas as pd
import os
from market_cap_export import download_market_cap_history  # Import only the function

# Define the path to the CSV file
file_path = "data/index-holdings-xlv.csv"

# Load the CSV file properly
try:
    df = pd.read_csv(file_path)  # Correct method for CSV
    print(df.head())  # Debugging: Show first few rows
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()

# Ensure the first column is 'Ticker' (or rename it if necessary)
expected_ticker_col = df.columns[0]  # Assuming first column has tickers
df.rename(columns={expected_ticker_col: "Ticker"}, inplace=True)

# Extract tickers, removing NaN values
tickers = df["Ticker"].dropna().astype(str).tolist()

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

