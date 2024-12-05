import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load the processed dataset (2016-2023 data)
file_path = 'processed_stock_articles_with_sentiment_2016-23.csv'
data = pd.read_csv(file_path)

# Ensure 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate percentage stock price change as the target (Close - Open)
data['Price_Change'] = (data['Close'] - data['Open']) / data['Open']

# Feature Engineering: Add lagged features and moving averages
data['Lag_1'] = data['Price_Change'].shift(1)
data['Lag_2'] = data['Price_Change'].shift(2)
data['MA_5'] = data['Price_Change'].rolling(5).mean()
data['MA_10'] = data['Price_Change'].rolling(10).mean()

# Drop rows with NaN values from feature engineering
data = data.dropna()

# Split data into training (2016-2022) and testing (2023)
train_data = data[data['Date'].dt.year <= 2022]
test_data = data[data['Date'].dt.year == 2023]

# Define features and target
features_without_sentiment = ['Open', 'Volume', 'Lag_1', 'Lag_2', 'MA_5', 'MA_10']
features_with_sentiment = features_without_sentiment + ['Sentiment_Score']
target = 'Price_Change'

X_train_no_sentiment = train_data[features_without_sentiment]
X_train_with_sentiment = train_data[features_with_sentiment]
y_train = train_data[target]

X_test_no_sentiment = test_data[features_without_sentiment]
X_test_with_sentiment = test_data[features_with_sentiment]
y_test = test_data[target]

# ---------------------------------------------------------
# RANDOM FOREST MODEL WITHOUT SENTIMENT
# ---------------------------------------------------------
rf_no_sentiment = RandomForestRegressor(n_estimators=100, random_state=42)
rf_no_sentiment.fit(X_train_no_sentiment, y_train)
y_pred_no_sentiment = rf_no_sentiment.predict(X_test_no_sentiment)

# Evaluate model without sentiment
mse_no_sentiment = mean_squared_error(y_test, y_pred_no_sentiment)
r2_no_sentiment = r2_score(y_test, y_pred_no_sentiment)
mae_no_sentiment = mean_absolute_error(y_test, y_pred_no_sentiment)

print("\nModel Without Sentiment - Evaluation Metrics:")
print(f"MSE: {mse_no_sentiment:.4f}, R²: {r2_no_sentiment:.4f}, MAE: {mae_no_sentiment:.4f}")

# ---------------------------------------------------------
# RANDOM FOREST MODEL WITH SENTIMENT
# ---------------------------------------------------------
rf_with_sentiment = RandomForestRegressor(n_estimators=100, random_state=42)
rf_with_sentiment.fit(X_train_with_sentiment, y_train)
y_pred_with_sentiment = rf_with_sentiment.predict(X_test_with_sentiment)

# Evaluate model with sentiment
mse_with_sentiment = mean_squared_error(y_test, y_pred_with_sentiment)
r2_with_sentiment = r2_score(y_test, y_pred_with_sentiment)
mae_with_sentiment = mean_absolute_error(y_test, y_pred_with_sentiment)

print("\nModel With Sentiment - Evaluation Metrics:")
print(f"MSE: {mse_with_sentiment:.4f}, R²: {r2_with_sentiment:.4f}, MAE: {mae_with_sentiment:.4f}")

# ---------------------------------------------------------
# VISUALIZATION
# ---------------------------------------------------------

# Create a comparison DataFrame for price changes
comparison_df = pd.DataFrame({
    'Date': test_data['Date'].values,
    'Actual Price Change': y_test.values,
    'Predicted Change (No Sentiment)': y_pred_no_sentiment,
    'Predicted Change (With Sentiment)': y_pred_with_sentiment
})

# Print the first few rows of the comparison table
print("\nComparison Table:")
print(comparison_df.head(10))

# Plot comparison of actual vs predicted price changes
plt.figure(figsize=(14, 8))
plt.plot(comparison_df['Date'], comparison_df['Actual Price Change'], label='Actual Price Change', color='blue', linewidth=2)
plt.plot(comparison_df['Date'], comparison_df['Predicted Change (No Sentiment)'], label='Predicted Change (No Sentiment)', color='green', linestyle='dashed', linewidth=2)
plt.plot(comparison_df['Date'], comparison_df['Predicted Change (With Sentiment)'], label='Predicted Change (With Sentiment)', color='red', linestyle='dashed', linewidth=2)

plt.xlabel('Date')
plt.ylabel('Price Change (Percentage)')
plt.title('Actual vs Predicted Price Changes (With and Without Sentiment)')
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# Select random 10 dates for detailed comparison
random_indices = np.random.choice(len(comparison_df), size=10, replace=False)
random_comparison = comparison_df.iloc[random_indices]

print("\nRandom Comparison of Predictions (10 Dates):")
print(random_comparison.to_string(index=False))

# Convert Price_Change into binary classes (1 for Increase, 0 for Decrease)
train_data['Direction'] = (train_data['Price_Change'] > 0).astype(int)
test_data['Direction'] = (test_data['Price_Change'] > 0).astype(int)

# Define features and target
X_train_no_sentiment = train_data[features_without_sentiment]
X_train_with_sentiment = train_data[features_with_sentiment]
y_train = train_data['Direction']

X_test_no_sentiment = test_data[features_without_sentiment]
X_test_with_sentiment = test_data[features_with_sentiment]
y_test = test_data['Direction']

# Train a Random Forest Classifier

rf_no_sentiment = RandomForestClassifier(n_estimators=100, random_state=42)
rf_no_sentiment.fit(X_train_no_sentiment, y_train)
y_pred_no_sentiment = rf_no_sentiment.predict(X_test_no_sentiment)

rf_with_sentiment = RandomForestClassifier(n_estimators=100, random_state=42)
rf_with_sentiment.fit(X_train_with_sentiment, y_train)
y_pred_with_sentiment = rf_with_sentiment.predict(X_test_with_sentiment)

# Evaluate models
accuracy_no_sentiment = accuracy_score(y_test, y_pred_no_sentiment)
accuracy_with_sentiment = accuracy_score(y_test, y_pred_with_sentiment)

print(f"Model Without Sentiment - Accuracy: {accuracy_no_sentiment:.2%}")
print(f"Model With Sentiment - Accuracy: {accuracy_with_sentiment:.2%}")
print("\nClassification Report Without Sentiment:\n", classification_report(y_test, y_pred_no_sentiment))
print("\nClassification Report With Sentiment:\n", classification_report(y_test, y_pred_with_sentiment))
