# Import necessary libraries
from pymongo import MongoClient
import pandas as pd
import urllib.parse

# Assuming 'df' is your DataFrame
df = pd.read_csv('Apple_stock_data.csv')

# Connect to MongoDB
password = "qwertyuiop"
client = MongoClient( f"mongodb+srv://EchoTrade:{password}@echo-trade.ujnvr.mongodb.net/?retryWrites=true&w=majority&appName=Echo-Trade")
db = client['Stock_Prices']
collection = db['Apple']  

# Convert DataFrame to dictionary
data = df.to_dict(orient='records')

# Insert data into MongoDB
result = collection.insert_many(data)

# Print the IDs of the inserted documents
print(result.inserted_ids)

# Close the client
client.close()