import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to format market cap
def format_market_cap(value):
    """
    Convert market cap strings like '1.5T' and '500B' into numerical values.
    """
    multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6}
    if value[-1] in multipliers:
        return float(value[:-1]) * multipliers[value[-1]]
    return float(value.replace(',', ''))

# Function to scrape and download market cap history
def download_market_cap_history(company_symbol):
    base_url = "https://www.marketcaphistory.com/"
    search_url = base_url + company_symbol.lower()
    
    try:
        # Fetch the webpage
        response = requests.get(search_url)
        response.raise_for_status()

        # Parse the webpage
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract market cap data
        outer_table = soup.find('table', class_='infotable')
        inner_table = outer_table.find('table')
        rows = inner_table.find_all('tr')

        market_cap_data = []
    
        for index, row in enumerate(rows):
            if index == 0:  # Skip the header row
                continue

            cells = row.find_all('td')
            if cells:
                date = pd.to_datetime(cells[0].get_text(strip=True)).strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD
                market_cap = format_market_cap(cells[1].get_text(strip=True))  # Convert to number

                market_cap_data.append([company_symbol.upper(), date, market_cap])
        
        print(f"Got {company_symbol} data")

        # Create a DataFrame 
        df = pd.DataFrame(market_cap_data, columns=["Company", "Date", "Market Cap"])
        
        # Ensure the data folder exists
        os.makedirs("companies_market_cap_data", exist_ok=True)
        
        # Save to CSV
        filename = f"xlv_market_cap_data/{company_symbol.upper()}_market_cap.csv"
        df.to_csv(filename, index=False)
        
        print(f"Data saved to xlv_market_cap_data/{filename}")
    
    except Exception as e:
        print(f"Error scraping data for {company_symbol}: {e}")

