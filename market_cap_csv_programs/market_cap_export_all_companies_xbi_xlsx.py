import pandas as pd
import os
from market_cap_export import download_market_cap_history  # Import only the function

# Define the path to the Excel file
file_path = "data/xbi-tickers-03-Feb-2025.xlsx"

# Load the second tab (tickers)
try:
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[1])  # Load the second sheet
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Ensure the 'Ticker' column exists
ticker_column = df.columns[0]  # Assuming first column has tickers
tickers = df[ticker_column].dropna().astype(str).tolist()  # Convert to list and remove NaN values

# Create a directory to store the output if it doesn’t exist
os.makedirs("companies_market_cap_data", exist_ok=True)

# Loop through each ticker and call the function
for ticker in tickers:
    print(f"Processing market cap history for {ticker}...")
    download_market_cap_history(ticker)

print("All tickers processed successfully.")

