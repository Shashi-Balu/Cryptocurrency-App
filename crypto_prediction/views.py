from django.shortcuts import render
from .coingecko import fetch_historical_data
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import numpy as np
import csv
import os

def save_historical_data_to_csv(coin_id, prices):
    file_path = f'data/{coin_id}_historical_prices.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'price'])
        for i, price in enumerate(prices):
            writer.writerow([i, price])

def load_historical_data_from_csv(coin_id):
    file_path = f'data/{coin_id}_historical_prices.csv'
    prices = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                prices.append(float(row[1]))
    return prices

def predict_crypto_price(request):
    # Define the top cryptocurrencies by their IDs
    crypto_ids = ['bitcoin', 'ethereum', 'solana', 'dogecoin', 'ripple', 'cardano', 'litecoin','tether','usdc','bnb','xrp','toncoin']
    
    days = 365  # Fetch historical data for the last 365 days

    # Fetch historical data and predict prices for each cryptocurrency
    future_prices_dict = {}
    for coin_id in crypto_ids:
        try:
            historical_prices = fetch_historical_data(coin_id, days)

            # Save fetched data to CSV for future use
            save_historical_data_to_csv(coin_id, historical_prices)

        except KeyError:
            print(f"KeyError: Using fallback data for {coin_id}")
            historical_prices = load_historical_data_from_csv(coin_id)

        if not historical_prices:
            print(f"No historical data available for {coin_id}. Skipping.")
            continue

        # Preprocess data
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_scaled = scaler.fit_transform(np.array(historical_prices).reshape(-1, 1))

        # Train model
        X = np.arange(len(data_scaled)).reshape(-1, 1)
        y = data_scaled
        model = LinearRegression()
        model.fit(X, y)

        # Predict future prices (next 7 days)
        future_prices = []
        for i in range(1, 8):
            future_price = model.predict(np.array([[len(historical_prices) + i]]))
            future_prices.append(scaler.inverse_transform(future_price)[0][0])

        future_prices_dict[coin_id] = future_prices

    context = {
        'future_prices_dict': future_prices_dict
    }
    return render(request, 'crypto_prediction/prediction.html', context)
