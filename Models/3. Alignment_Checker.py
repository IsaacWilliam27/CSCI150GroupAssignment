import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'processed_stock_articles_with_sentiment_2016-23.csv'
data = pd.read_csv(file_path)

# Ensure 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate price change (Close - Open)
data['Price_Change'] = data['Close'] - data['Open']

# Sort data by date to ensure it's in proper order
data = data.sort_values(by='Date')

# Define the window to check the price change trend (e.g., 3 days after the article)
window = 3

# Shift price change to check the window of days after the article
for i in range(1, window + 1):
    data[f'Price_Change_Day_{i}'] = data['Price_Change'].shift(-i)

# Check if positive sentiment led to a price increase in the next 3 days
def check_positive_alignment(row):
    if row['Sentiment_Score'] > 0:
        # Look for a price increase in the next 3 days
        price_trend = [row[f'Price_Change_Day_{i}'] for i in range(1, window + 1)]
        if any(change > row['Price_Change'] for change in price_trend):
            return 'Aligned Positive'
    elif row['Sentiment_Score'] < 0:
        # Look for a price decrease in the next 3 days
        price_trend = [row[f'Price_Change_Day_{i}'] for i in range(1, window + 1)]
        if any(change < row['Price_Change'] for change in price_trend):
            return 'Aligned Negative'
    return 'Not Aligned'

# Apply the function to determine alignment
data['Alignment'] = data.apply(check_positive_alignment, axis=1)

# Filter aligned data
aligned_data = data[data['Alignment'] != 'Not Aligned']

# Analyze the percentage of aligned articles
total_articles = len(data)
aligned_articles = len(aligned_data)
alignment_percentage = (aligned_articles / total_articles) * 100
print(f"Final Alignment Percentage: {alignment_percentage:.2f}%")
print("Articles aligned: ", aligned_articles, "out of ", total_articles)

# Save aligned data to an Excel file
aligned_data.to_excel('aligned_articles.xlsx', index=False)

