import requests
import pandas as pd
import numpy as np
import yfinance as yf  # Importing yfinance for Yahoo Finance data

# Function to get stock data from Yahoo Finance (from 2014 to now)
def get_stock_data(stock_symbol):
    start_date = '2014-01-01'
    end_date = '2022-12-31'
  
    # Fetch data from Yahoo Finance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    if stock_data.empty:
        print(f"No data available for the selected period.")
        return None
  
    return stock_data

# Main script to tie everything together
if __name__ == '__main__':
    stock_symbol = 'AAPL'
    company_name = 'Apple'

    # Fetch stock data from 2014 to 2022
    stock_data = get_stock_data(stock_symbol)

    if stock_data is not None:
        # Display stock data in tabular format
        print("\nStock Data:")
        print(stock_data)

        print("\nStock Data with Date Index:")
        print(stock_data[['Open', 'High', 'Low', 'Close', 'Volume']])
        
        # Save the stock data to a CSV file
        csv_file_name = f"{company_name}_stock_data.csv"
        stock_data.to_csv(csv_file_name)
        print(f"\nStock data has been saved to '{csv_file_name}'.")