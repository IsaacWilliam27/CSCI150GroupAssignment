import os
import pandas as pd


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

# Function to combine all months' article data for a given year into one DataFrame
def combine_article_data_for_year(year):
    all_months_data = []
    for month in months:
        article_file = f'Articles {year}/apple_financial_articles_with_sentiment_{month}_{year}.csv'
        if os.path.exists(article_file):
            try:
                # Load the article data
                articles_df = pd.read_csv(article_file, encoding='ISO-8859-1')

                # Ensure only necessary columns are kept
                if 'Date' in articles_df.columns and 'Title' in articles_df.columns and 'Content' in articles_df.columns:
                    articles_df = articles_df[['Date', 'Title', 'Content']]

                    # Try converting the 'Date' column to datetime, errors='coerce' will turn invalid dates into NaT
                    articles_df['Date'] = pd.to_datetime(articles_df['Date'], errors='coerce')

                    # Drop rows where 'Date' is NaT (invalid or missing dates)
                    valid_articles_df = articles_df.dropna(subset=['Date'])

                    # Log how many rows were dropped due to invalid dates
                    invalid_rows = len(articles_df) - len(valid_articles_df)
                    if invalid_rows > 0:
                        print(f"{invalid_rows} invalid date rows skipped in {article_file}")

                    # Append the valid data
                    all_months_data.append(valid_articles_df)
                else:
                    print(f"Required columns missing in {article_file}. Skipping...")
            except Exception as e:
                print(f"Error reading {article_file}: {e}")
        else:
            print(f"File {article_file} does not exist.")

  
    if all_months_data:
        combined_articles_df = pd.concat(all_months_data, ignore_index=True)
        return combined_articles_df
    else:
        print(f"No data for {year}.")
        return None

# Function to merge article data with stock data for a given year
def merge_with_stock_data(year):
    # Combine article data for the year
    articles_df = combine_article_data_for_year(year)
    
    # Load stock price data
    stock_file = f'Articles {year}/Apple_stock_price_{year}.csv'
    if os.path.exists(stock_file):
        try:
            stock_prices_df = pd.read_csv(stock_file, encoding='ISO-8859-1')
            stock_prices_df['Date'] = pd.to_datetime(stock_prices_df['Date'], format='%d-%b-%y', errors='coerce')
            stock_prices_df['Volume'] = stock_prices_df['Volume'].str.replace(',', '').astype(float)
            stock_prices_df['Price_Change'] = stock_prices_df['Close'] - stock_prices_df['Open']

            # Drop rows with invalid dates in stock data
            stock_prices_df = stock_prices_df.dropna(subset=['Date'])
        except Exception as e:
            print(f"Error processing stock data in {stock_file}: {e}")
            return None
    else:
        print(f"Stock file {stock_file} does not exist.")
        return None

    # Merge articles with stock prices on 'Date'
    if articles_df is not None and not articles_df.empty:
        merged_df = pd.merge(articles_df, stock_prices_df, on='Date', how='inner')
        return merged_df
    else:
        print(f"No articles available for {year}.")
        return None

# Function to process all years and combine data
def combine_all_years_data(start_year, end_year):
    all_years_data = []
    for year in range(start_year, end_year + 1):
        print(f"Processing year {year}...")
        year_data = merge_with_stock_data(year)
        if year_data is not None:
            all_years_data.append(year_data)

    if all_years_data:
        combined_df = pd.concat(all_years_data, ignore_index=True)
        return combined_df
    else:
        print("No valid data found for any year.")
        return None


def main():
    # Process data from 2016 to 2023
    combined_data = combine_all_years_data(2016, 2023)


    if combined_data is not None:
        combined_data.to_csv('combined_stock_articles_2016_2023.csv', index=False)
        print("Combined data saved to 'combined_stock_articles_2016_2023.csv'.")
    else:
        print("No data combined.")


# Load the dataset
file_path = 'combined_stock_articles_2016_2023.csv'
data = pd.read_csv(file_path)


data['Date'] = pd.to_datetime(data['Date'])

# Calculate percentage stock price change
data['Price_Change'] = (data['Close'] - data['Open']) / data['Open']

# Sort data by date to ensure everything is in order
data = data.sort_values(by='Date')

# Add moving averages of stock price changes (e.g., 5-day and 10-day moving averages)
data['MA_5'] = data['Price_Change'].rolling(window=5).mean()
data['MA_10'] = data['Price_Change'].rolling(window=10).mean()



if __name__ == "__main__":
    main()
