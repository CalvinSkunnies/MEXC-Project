import requests
import time
import csv

def get_mexc_usd_pairs_flat(allowed_quotes=("USDT", "USDC")):
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    token_rows = []

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
            quote_asset = symbol.get("quoteAsset")
            symbol_name = symbol.get("symbol")

            if base_asset and quote_asset in allowed_quotes and symbol_name:
                # Each row is Token ID (symbol), Token Name (base asset), Ticker (symbol)
                token_rows.append([base_asset, symbol_name])

        print(f"✅ Total USDT/USDC trading pairs: {len(token_rows)}")

        # Save to CSV
        with open("MEXCTokens.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Token Name", "Ticker"])
            for row in token_rows:
                writer.writerow(row)

        print("💾 Data saved to MEXCTokens.csv")
        return token_rows

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return []

if __name__ == "__main__":
    tokens = get_mexc_usd_pairs_flat()
    for row in tokens[:10]:  # Show first 10 rows
        print(row)
