import requests
import pandas as pd
import time
from datetime import datetime, timezone

def get_valid_symbols():
    url = 'https://api.mexc.com/api/v3/exchangeInfo'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {item['symbol'] for item in data['symbols']}

def fetch_ohlcv(symbol: str, interval: str = '1w', start_time: int = None):
    url = 'https://api.mexc.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1000
    }
    if start_time:
        params['startTime'] = start_time

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['symbol'] = symbol
        return df[['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# ------------------ USER SETTINGS ------------------

base_tokens = ['BROCK', 'BNT', 'NTX', 'DEVVE']  # Tokens without quote asset
quote_asset = 'USDT'
interval = '1w'

# Date range: 2025-01-01 to now
start_dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
start_timestamp = int(start_dt.timestamp() * 1000)

# ------------------ RUN ------------------

valid_symbols = get_valid_symbols()

all_data = []
for token in base_tokens:
    pair = f"{token.upper()}{quote_asset}"
    if pair in valid_symbols:
        df = fetch_ohlcv(pair, interval=interval, start_time=start_timestamp)
        if df is not None:
            all_data.append(df)
    else:
        print(f"Pair {pair} not found on MEXC.")

# Save to CSV
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('mexc_ohlcv_weekly.csv', index=False)
    print("Data saved to MEXC_OHLCV.csv")
else:
    print("No valid data fetched.")
