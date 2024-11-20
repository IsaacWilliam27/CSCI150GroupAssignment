import yfinance as yf
from pymongo import MongoClient

# Reconnect to MongoDB using the same credentials
password = "qwertyuiop"
client = MongoClient(f"mongodb+srv://EchoTrade:{password}@echo-trade.ujnvr.mongodb.net/?retryWrites=true&w=majority&appName=Echo-Trade")
db = client['Stock_Prices']
collection = db['Apple']

# Step 1: Let user input 8 dates for comparison
chosen_dates = []
print("Please enter 8 dates (in format YYYY-MM-DD) between 2014 and 2022:")
for i in range(8):
    date = input(f"Enter date {i + 1}: ")
    chosen_dates.append(date)

# Step 2: Fetch data from yfinance for the chosen dates
print("\nFetching stock data from Yahoo Finance...")
ticker = 'AAPL'
data = yf.download(ticker, start='2014-01-01', end='2022-12-31')

# Step 3: Check if data matches between yfinance and MongoDB for those dates
for date in chosen_dates:
    # Check if date is in the yfinance data
    if date in data.index:
        yfinance_data = data.loc[date].to_dict()  # Get the row from yfinance data
    else:
        print(f"{date} is not in the fetched data from Yahoo Finance.")
        continue

    # Fetch data from MongoDB for the same date
    mongo_data = collection.find_one({"Date": date})

    print(f"\nTesting for Date: {date}")

    # Compare values between yfinance and MongoDB, rounding to 10 decimal places
    match = True
    for key in yfinance_data:
        # Round the values to 10 decimal places for comparison
        yfinance_value = round(yfinance_data[key], 2)
        mongo_value = round(mongo_data[key], 2) if key in mongo_data else None

        if mongo_value is not None and yfinance_value != mongo_value:
            match = False
            print(f"Mismatch found for {key}: yfinance = {yfinance_value}, MongoDB = {mongo_value}")

    if match:
        print(f"All values match for {date}!")
    else:
        print(f"Values do not match for {date}.")

# Close the client connection
client.close()
