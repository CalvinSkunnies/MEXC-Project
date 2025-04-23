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

def get_order_book(symbol, limit=1000):
    url = f"https://api.mexc.com/api/v3/depth"
    params = {
        "symbol": symbol,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("bids", []), data.get("asks", [])
    except Exception as e:
        print(f"❌ Error fetching depth for {symbol}: {e}")
        return [], []

def calculate_depth_plus_minus_2_percent(symbol):
    bids, asks = get_order_book(symbol)

    if not bids or not asks:
        return 0, 0

    try:
        best_bid = float(bids[0][0])
        best_ask = float(asks[0][0])
        mid_price = (best_bid + best_ask) / 2

        lower_bound = mid_price * 0.98
        upper_bound = mid_price * 1.02

        # Depth -2% (Buy liquidity)
        buy_depth = sum(float(price) * float(qty)
                        for price, qty in bids
                        if float(price) >= lower_bound)

        # Depth +2% (Sell liquidity)
        sell_depth = sum(float(price) * float(qty)
                         for price, qty in asks
                         if float(price) <= upper_bound)

        return buy_depth, sell_depth
    except Exception as e:
        print(f"❌ Error calculating depth for {symbol}: {e}")
        return 0, 0

def merge_and_save():
    tokens = get_token_pairs_usd()
    stats = get_24hr_stats()

    filename = "MEXCData.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Token Name", "Ticker", "Pair", "Symbol",
            "Price Change", "% Change", "Last Price",
            "Volume", "Quote Volume", "High", "Low", "Open Price",
            "Bid Price", "Ask Price",
            "Depth -2%", "Depth +2%"
        ])

        for token in tokens:
            symbol = token["Symbol"]
            data = stats.get(symbol, {})

            # Pull order book depth data
            buy_depth, sell_depth = calculate_depth_plus_minus_2_percent(symbol)

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
                data.get("openPrice", ""),
                data.get("bidPrice", ""),
                data.get("askPrice", ""),
                round(buy_depth, 2),
                round(sell_depth, 2)
            ])
            time.sleep(0.1)  # small delay to avoid rate limit

    print(f"✅ Final MEXC CSV saved as: {filename}")

if __name__ == "__main__":
    merge_and_save()
