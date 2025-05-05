import requests
import csv
import time

def fetch_mexc_ohlcv(symbol, interval="1h", limit=50):
    url = "https://api.mexc.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        raw = response.json()

        return [
            {
                "Time": time.strftime('%Y-%m-%d %H:%M', time.gmtime(entry[0] // 1000)),
                "Open": float(entry[1]),
                "High": float(entry[2]),
                "Low": float(entry[3]),
                "Close": float(entry[4]),
                "Volume": float(entry[5]),
                "Symbol": symbol
            }
            for entry in raw
        ]

    except Exception as e:
        print(f"❌ Failed to fetch {symbol}: {e}")
        return []

def save_to_csv(data, filename="MEXC_OHLV.csv"):
    if not data:
        print("No data to save.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Saved OHLCV to {filename}")

def main():
    # Example token symbols (you can load this list from a file or from CoinGecko IDs)
    base_symbols = ["ETH", "DOGE", "PEPE", "SOL"]  # Replace with actual base symbols
    quote = "USDT"

    all_data = []
    for base in base_symbols:
        trading_pair = base.upper() + quote
        ohlcv = fetch_mexc_ohlcv(trading_pair)
        all_data.extend(ohlcv)
        time.sleep(0.5)

    save_to_csv(all_data)

if __name__ == "__main__":
    main()
