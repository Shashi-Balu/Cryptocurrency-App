# crypto_prediction/coingecko.py
import requests

def fetch_historical_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = [entry[1] for entry in data['prices']]
    return prices
