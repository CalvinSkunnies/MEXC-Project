import requests
import time
import csv

def get_token_pairs_usd():
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    headers = { "User-Agent": "Chrome/5.0" }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    symbols = response.json().get("symbols", [])
    token_rows = []

    for symbol in symbols:
        base = symbol.get("baseAsset")
        quote = symbol.get("quoteAsset")
        if quote in ("USDT", "USDC"):
            token_rows.append({
                "Token Name": base,
                "Ticker": base,
                "Pair": quote,
                "Symbol": base + quote
            })

    return token_rows

def get_24hr_stats():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    stats = response.json()
    return { item["symbol"]: item for item in stats }

def merge_and_save():
    tokens = get_token_pairs_usd()
    stats = get_24hr_stats()

    filename = "MEXCData.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Token Name", "Ticker", "Pair", "Symbol",
            "Price Change", "% Change", "Last Price",
            "Volume", "Quote Volume", "High", "Low", "Open Price"
        ])

        for token in tokens:
            symbol = token["Symbol"]
            data = stats.get(symbol, {})

            writer.writerow([
                token["Token Name"],
                token["Ticker"],
                token["Pair"],
                symbol,
                data.get("priceChange", ""),
                data.get("priceChangePercent", ""),
                data.get("lastPrice", ""),
                data.get("volume", ""),
                data.get("quoteVolume", ""),
                data.get("highPrice", ""),
                data.get("lowPrice", ""),
                data.get("openPrice", "")
            ])

    print(f"✅ Merged CSV saved as {filename}")

if __name__ == "__main__":
    merge_and_save()
