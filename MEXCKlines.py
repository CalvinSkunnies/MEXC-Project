import requests
import pandas as pd
import time
from datetime import datetime, timezone

# 🔐 Replace with your actual MEXC API Key
API_KEY = 'mx0vglMdf1KwfydbVr'

# Configuration
base_tokens = ['BROCK', 'BNT', 'NTX', 'DEVVE']
quote_assets = ['USDT', 'USDC']
interval = '1d'
start_date = '2025-01-01'
start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp() * 1000)

# Rate limiter
def rate_limit_sleep():
    time.sleep(0.21)  # 0.21s delay = ~4.76 requests/sec

# Get valid trading pairs
def get_valid_symbols():
    url = 'https://api.mexc.com/api/v3/exchangeInfo'
    headers = {
        'X-MEXC-API-KEY': API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {item['symbol'] for item in data['symbols']}
    except Exception as e:
        print(f"Error getting valid symbols: {e}")
        return set()

# Fetch OHLCV
def fetch_ohlcv(symbol: str, interval: str = '1h', start_time: int = None, limit: int = 500):
    url = 'https://api.mexc.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    if start_time:
        params['startTime'] = start_time

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['symbol'] = symbol
        return df[['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching OHLCV for {symbol}: {e}")
        return None

# ------------------- Main Script -------------------

valid_symbols = get_valid_symbols()
rate_limit_sleep()  # Respect rate limit

all_data = []

for token in base_tokens:
    found = False
    for quote in quote_assets:
        pair = f"{token.upper()}{quote}"
        if pair in valid_symbols:
            df = fetch_ohlcv(pair, interval=interval, start_time=start_timestamp)
            rate_limit_sleep()  # Respect rate limit after each request

            if df is not None and not df.empty:
                df['pair'] = f"{token.upper()}/{quote}"
                all_data.append(df)
                print(f"✅ Fetched: {pair}")
                found = True
                break
            else:
                print(f"⚠️ No data for {pair}")
        else:
            print(f"⏭️ Skipping unavailable pair: {pair}")
    if not found:
        print(f"❌ No valid pair found for {token}")

# Save to CSV
if all_data:
    result_df = pd.concat(all_data, ignore_index=True)
    result_df.to_csv('MEXCKlines.csv', index=False)
    print("✅ Data saved to MEXCKlines.csv")
else:
    print("❌ No data to save.")
