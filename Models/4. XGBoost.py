import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np

# Load the processed dataset (2016-2022 data)
file_path = 'processed_stock_articles_with_sentiment_2016-23.csv'
data = pd.read_csv(file_path)

# Ensure 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate percentage stock price change as the target (Close - Open)
data['Price_Change'] = (data['Close'] - data['Open']) / data['Open']

# Drop rows with NaN values
data = data.dropna()

# Split data into training (2016-2022) and testing (2023) sets
train_data = data[data['Date'].dt.year <= 2022]
test_data = data[data['Date'].dt.year == 2023]

# Define the feature sets
features_without_sentiment = ['Open', 'Volume']
features_with_sentiment = ['Open', 'Volume', 'Sentiment_Score']

# Target variable
y_train = train_data['Price_Change']
y_test = test_data['Price_Change']

# ---------------------------------------------------------
# MODEL WITHOUT SENTIMENT
# ---------------------------------------------------------
X_train_no_sentiment = train_data[features_without_sentiment]
X_test_no_sentiment = test_data[features_without_sentiment]

xgb_model_no_sentiment = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
xgb_model_no_sentiment.fit(X_train_no_sentiment, y_train)
y_pred_no_sentiment = xgb_model_no_sentiment.predict(X_test_no_sentiment)

# Evaluate the model without sentiment
mse_no_sentiment = mean_squared_error(y_test, y_pred_no_sentiment)
r2_no_sentiment = r2_score(y_test, y_pred_no_sentiment)
mae_no_sentiment = mean_absolute_error(y_test, y_pred_no_sentiment)
accuracy_no_sentiment = 100 * (1 - mae_no_sentiment)

# ---------------------------------------------------------
# MODEL WITH SENTIMENT
# ---------------------------------------------------------
X_train_with_sentiment = train_data[features_with_sentiment]
X_test_with_sentiment = test_data[features_with_sentiment]

xgb_model_with_sentiment = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
xgb_model_with_sentiment.fit(X_train_with_sentiment, y_train)
y_pred_with_sentiment = xgb_model_with_sentiment.predict(X_test_with_sentiment)

# Evaluate the model with sentiment
mse_with_sentiment = mean_squared_error(y_test, y_pred_with_sentiment)
r2_with_sentiment = r2_score(y_test, y_pred_with_sentiment)
mae_with_sentiment = mean_absolute_error(y_test, y_pred_with_sentiment)
accuracy_with_sentiment = 100 * (1 - mae_with_sentiment)

# ---------------------------------------------------------
# RANDOM 10 DATES FOR COMPARISON
# ---------------------------------------------------------
random_indices = np.random.choice(len(test_data), size=10, replace=False)
comparison_df = pd.DataFrame({
    'Date': test_data['Date'].iloc[random_indices].values,
    'Actual Price Change': y_test.iloc[random_indices].values,
    'Predicted Without Sentiment': y_pred_no_sentiment[random_indices],
    'Predicted With Sentiment': y_pred_with_sentiment[random_indices]
})

# comparison table
print("\nComparison Table (Random 10 Dates):")
print(comparison_df.to_string(index=False))

# Print evaluation metrics
print("\nModel Evaluation Metrics:")
print(f"Model Without Sentiment - MSE: {mse_no_sentiment:.4f}, R²: {r2_no_sentiment:.4f}, MAE: {mae_no_sentiment:.4f}, Accuracy: {accuracy_no_sentiment:.2f}%")
print(f"Model With Sentiment - MSE: {mse_with_sentiment:.4f}, R²: {r2_with_sentiment:.4f}, MAE: {mae_with_sentiment:.4f}, Accuracy: {accuracy_with_sentiment:.2f}%")

# ---------------------------------------------------------
# VISUALIZATION 
# ---------------------------------------------------------
plt.figure(figsize=(14, 8))
plt.plot(test_data['Date'], y_test, label='Actual Price Change', color='blue', linewidth=2)
plt.plot(test_data['Date'], y_pred_no_sentiment, label='Predicted Without Sentiment', color='green', linestyle='dashed', linewidth=2)
plt.plot(test_data['Date'], y_pred_with_sentiment, label='Predicted With Sentiment', color='red', linestyle='dashed', linewidth=2)

plt.xlabel('Date')
plt.ylabel('Price Change')
plt.title('Actual vs Predicted Price Change (With and Without Sentiment)', fontsize=16)
plt.legend(fontsize=12)
plt.xticks(rotation=45, fontsize=12)
plt.tight_layout()
plt.show()
