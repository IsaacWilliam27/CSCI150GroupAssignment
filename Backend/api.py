from pymongo import MongoClient
import urllib.parse
import requests
from datetime import datetime
import yfinance as yf  # Importing yfinance for Yahoo Finance data
import pandas as pd

# MongoDB connection details
password = urllib.parse.quote("qwertyuiop")  # You can use the 'AAPL' password
uri = f"mongodb+srv://EchoTrade:<db_password>@echo-trade.ujnvr.mongodb.net/?retryWrites=true&w=majority&appName=Echo-Trade"
client = MongoClient(uri)

# Database and collection references
db = client['Stock_Prices']  # database name
collection = db['Apple']     # collection name

# Function to get stock data from Yahoo Finance (from 2014 to 2022)
def get_stock_data(stock_symbol):
    start_date = '2014-01-01'
    end_date = '2022-12-31'
    
    # Fetch data from Yahoo Finance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    if stock_data.empty:
        print(f"No data available for the selected period.")
        return None
    
    return stock_data

# Function to insert stock data into MongoDB
def insert_stock_data_to_mongo(stock_data, collection):
    stock_data.reset_index(inplace=True)  # Reset index to get 'Date' as a column

    # Preparing data to insert into MongoDB
    for index, row in stock_data.iterrows():
        stock_entry = {
            "date": row['Date'].strftime('%Y-%m-%d'),  # Format date to a string
            "open": row['Open'],
            "close": row['Close'],
            "volume": row['Volume']
        }
        # Inserting into MongoDB
        collection.insert_one(stock_entry)

    print("Stock data inserted into MongoDB successfully.")

# Main script to tie everything together
if __name__ == '__main__':
    stock_symbol = 'AAPL'  # Apple stock symbol
    
    # Fetching stock data from 2014 to 2022
    stock_data = get_stock_data(stock_symbol)
    if stock_data is not None:
        # Inserting stock data into MongoDB
        insert_stock_data_to_mongo(stock_data, collection)
