import requests
import time
import csv

def get_all_mexc_usd_pairs(allowed_quotes=("USDT", "USDC")):
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    token_rows = []
    seen_pairs = set()

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

            if base_asset and quote_asset in allowed_quotes:
                pair_key = f"{base_asset}_{quote_asset}"

                if pair_key not in seen_pairs:
                    seen_pairs.add(pair_key)
                    token_rows.append([base_asset, base_asset, quote_asset])  # Token Name = Ticker = base_asset

        print(f"✅ Total USDT/USDC trading pairs: {len(token_rows)}")

        # Save to CSV
        with open("MEXCTokens.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Token Name", "Ticker", "Pair"])
            for row in token_rows:
                writer.writerow(row)

        print("💾 Data saved to MEXCTokens.csv")
        return token_rows

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return []

if __name__ == "__main__":
    token_data = get_all_mexc_usd_pairs()
    for row in token_data[:10]:  # preview first 10
        print(row)
