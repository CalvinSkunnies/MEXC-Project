import requests
import time
import csv
from collections import defaultdict

def get_filtered_mexc_tokens_and_tickers(allowed_quotes=("USDT", "USDC")):
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    token_ticker_map = defaultdict(list)

    headers = {
        "User-Agent": "Chrome/5.0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(0.75)
        response.raise_for_status()
        data = response.json()
        symbols = data.get("symbols", [])

        for symbol in symbols:
            base_asset = symbol.get("baseAsset")
            quote_asset = symbol.get("quoteAsset")
            symbol_name = symbol.get("symbol")

            # Only allow USDT/USDC quoted pairs
            if base_asset and quote_asset in allowed_quotes and symbol_name:
                token_ticker_map[base_asset].append(symbol_name)

        print(f"✅ Total unique base tokens (USDT/USDC only): {len(token_ticker_map)}\n")

        # Save to CSV
        with open("MEXC_USD_Tokens_and_Tickers.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Token", "Tickers"])  # Header
            for token, tickers in sorted(token_ticker_map.items()):
                writer.writerow([token, ", ".join(tickers)])

        print("💾 Data saved to MEXCTokens.csv")
        return token_ticker_map

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {}

if __name__ == "__main__":
    token_map = get_filtered_mexc_tokens_and_tickers()
    for token, tickers in list(token_map.items())[:10]:  # Preview first 10
        print(f"{token}: {tickers}")
