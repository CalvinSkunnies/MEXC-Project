import requests
import pandas as pd
from datetime import datetime, timezone

# Base tokens (no quote asset)
base_tokens = ['BROCK', 'BNT', 'NTX', 'DEVVE']
quote_assets = ['USDT', 'USDC', 'ETH', 'MX']
interval = '1w'
start_date = '2025-01-01'
start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp() * 1000)

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
        if not data:
            return None
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['symbol'] = symbol
        return df[df['timestamp'] >= pd.to_datetime(start_date)][['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# ------------------- Main -------------------

valid_symbols = get_valid_symbols()
all_data = []

for token in base_tokens:
    found = False
    for quote in quote_assets:
        pair = f"{token.upper()}{quote}"
        if pair in valid_symbols:
            df = fetch_ohlcv(pair, interval=interval, start_time=start_timestamp)
            if df is not None and not df.empty:
                all_data.append(df)
                print(f"✅ Fetched: {pair}")
                found = True
                break  # stop checking other quote assets
            else:
                print(f"⚠️ No data for {pair}")
    if not found:
        print(f"❌ No valid pair found for {token}")

# Save to CSV
if all_data:
    result_df = pd.concat(all_data, ignore_index=True)
    result_df.to_csv('mexc_ohlcv.csv', index=False)
    print("✅ Saved to mexc_ohlcv.csv")
else:
    print("❌ No data to save.")
