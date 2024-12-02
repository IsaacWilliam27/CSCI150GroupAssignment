import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# Load the dataset (assuming the file has been preprocessed)
file_path = 'processed_stock_articles_with_sentiment_2016-23.csv'
data = pd.read_csv(file_path)

# Ensure 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate percentage stock price change as the target (Close - Open)
data['Price_Change'] = (data['Close'] - data['Open']) / data['Open']

# Drop rows with NaN values
data = data.dropna()

# Select features and target
features_without_sentiment = ['Open', 'Close', 'Volume']  # Without sentiment
features_with_sentiment = ['Open', 'Close', 'Volume', 'Sentiment_Score']  # With sentiment

# MinMax Scaling to normalize the features
scaler = MinMaxScaler()

# Function to create sequences of features for LSTM
def create_sequences(data, target, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(target[i + window_size])
    return np.array(X), np.array(y)

# Function to build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))  # Output layer for price change prediction
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Parameters
window_size = 60  # We will use the past 60 days of data to predict the next day

# Train/Test Split
train_data = data[data['Date'].dt.year <= 2022]
test_data = data[data['Date'].dt.year == 2023]

# Features and target for training/testing
X_train_no_sentiment = train_data[features_without_sentiment]
y_train = train_data['Price_Change']

X_test_no_sentiment = test_data[features_without_sentiment]
y_test = test_data['Price_Change']

X_train_with_sentiment = train_data[features_with_sentiment]
X_test_with_sentiment = test_data[features_with_sentiment]

# Scale the data
X_train_no_sentiment_scaled = scaler.fit_transform(X_train_no_sentiment)
X_test_no_sentiment_scaled = scaler.transform(X_test_no_sentiment)

X_train_with_sentiment_scaled = scaler.fit_transform(X_train_with_sentiment)
X_test_with_sentiment_scaled = scaler.transform(X_test_with_sentiment)

# Create sequences for LSTM
X_train_seq_no_sentiment, y_train_seq = create_sequences(X_train_no_sentiment_scaled, y_train.values, window_size)
X_test_seq_no_sentiment, y_test_seq = create_sequences(X_test_no_sentiment_scaled, y_test.values, window_size)

X_train_seq_with_sentiment, _ = create_sequences(X_train_with_sentiment_scaled, y_train.values, window_size)
X_test_seq_with_sentiment, _ = create_sequences(X_test_with_sentiment_scaled, y_test.values, window_size)

# Build and train LSTM model (without sentiment)
model_no_sentiment = build_lstm_model((X_train_seq_no_sentiment.shape[1], X_train_seq_no_sentiment.shape[2]))
model_no_sentiment.fit(X_train_seq_no_sentiment, y_train_seq, epochs=10, batch_size=32)

# Predict on test data (without sentiment)
y_pred_no_sentiment = model_no_sentiment.predict(X_test_seq_no_sentiment)

# Reshape predictions
y_pred_no_sentiment = y_pred_no_sentiment.flatten()

# Calculate performance metrics (without sentiment)
mse_no_sentiment = mean_squared_error(y_test_seq, y_pred_no_sentiment)
r2_no_sentiment = r2_score(y_test_seq, y_pred_no_sentiment)
mae_no_sentiment = mean_absolute_error(y_test_seq, y_pred_no_sentiment)

print(f'LSTM Model Without Sentiment - MSE: {mse_no_sentiment}, R2: {r2_no_sentiment}, MAE: {mae_no_sentiment}')

# Build and train LSTM model (with sentiment)
model_with_sentiment = build_lstm_model((X_train_seq_with_sentiment.shape[1], X_train_seq_with_sentiment.shape[2]))
model_with_sentiment.fit(X_train_seq_with_sentiment, y_train_seq, epochs=10, batch_size=32)

# Predict on test data (with sentiment)
y_pred_with_sentiment = model_with_sentiment.predict(X_test_seq_with_sentiment)

# Reshape predictions
y_pred_with_sentiment = y_pred_with_sentiment.flatten()

# Calculate performance metrics (with sentiment)
mse_with_sentiment = mean_squared_error(y_test_seq, y_pred_with_sentiment)
r2_with_sentiment = r2_score(y_test_seq, y_pred_with_sentiment)
mae_with_sentiment = mean_absolute_error(y_test_seq, y_pred_with_sentiment)

print(f'LSTM Model With Sentiment - MSE: {mse_with_sentiment}, R2: {r2_with_sentiment}, MAE: {mae_with_sentiment}')

# Plot predictions for both models
plt.figure(figsize=(14, 7))
plt.plot(test_data['Date'].iloc[window_size:], y_test_seq, color='blue', label='Actual Price Change')
plt.plot(test_data['Date'].iloc[window_size:], y_pred_no_sentiment, color='orange', label='Predicted Without Sentiment')
plt.plot(test_data['Date'].iloc[window_size:], y_pred_with_sentiment, color='green', label='Predicted With Sentiment')
plt.title('Stock Price Prediction (2023) - LSTM')
plt.xlabel('Date')
plt.ylabel('Price Change')
plt.legend()
plt.show()
