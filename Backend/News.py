import pandas as pd
from pymongo import MongoClient

# Load the Excel file from the specified path
file_path = '/Users/lekhanadevi/Downloads/aligned_articles.xlsx'
excel_data = pd.read_excel(file_path, sheet_name='Sheet1')

# Select only the columns you need
filtered_data = excel_data[['Date', 'Title', 'Content', 'Sentiment_Score']]

# Connect to MongoDB
password = "qwertyuiop"
client = MongoClient(f"mongodb+srv://EchoTrade:{password}@echo-trade.ujnvr.mongodb.net/?retryWrites=true&w=majority&appName=Echo-Trade")
db = client['NewsData']
collection = db['Apple']

# Convert filtered DataFrame to a list of dictionaries
data_dict = filtered_data.to_dict(orient="records")

# Insert data into MongoDB collection
collection.insert_many(data_dict)
print("Selected data from Excel has been successfully inserted into MongoDB!")
