import requests
import pandas as pd
import time

# Config
API_KEY = "CG-MfMJsvzUhR8PtJfvvSRi1UEm"
BASE_URL = "https://pro-api.coingecko.com/api/v3"
HEADERS = {"x_cg_pro_api_key": API_KEY}

# Load your token names or symbols
def load_tokens(file_path):
    df = pd.read_csv(file_path)  # expects a column "Token"
    return df["Token Name"].dropna().tolist()

# Fetch full list of coins from CoinGecko (name, symbol, id)
def get_all_coins_list():
    url = f"{BASE_URL}/coins/list"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Match token name or symbol to CoinGecko ID
def match_token_ids(token_list, all_coins):
    matched = {}
    unmatched = []

    for token in token_list:
        token_lower = token.lower()
        match = next((coin for coin in all_coins if coin["symbol"] == token_lower or coin["name"].lower() == token_lower), None)
        if match:
            matched[token] = match["id"]
        else:
            unmatched.append(token)

    return matched, unmatched

# Fetch market data from CoinGecko for matched tokens
def fetch_market_data(matched_ids):
    ids = ",".join(matched_ids.values())
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ids
    }

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# Main script
def main():
    input_file = "MEXCData.csv"  # contains a column "Token"
    token_list = load_tokens(input_file)

    print("🔍 Fetching all tokens from CoinGecko...")
    all_coins = get_all_coins_list()

    print("🔗 Matching input tokens to CoinGecko IDs...")
    matched, unmatched = match_token_ids(token_list, all_coins)

    print(f"✅ Matched: {len(matched)} tokens")
    print(f"❌ Unmatched: {unmatched}")

    print("📊 Fetching market data for matched tokens...")
    data = fetch_market_data(matched)

    output = []
    for token in data:
        output.append({
            "Input Token": [k for k, v in matched.items() if v == token["id"]][0],
            "CoinGecko ID": token["id"],
            "Name": token["name"],
            "Symbol": token["symbol"],
            "Market Cap": token.get("market_cap"),
            "FDV": token.get("fully_diluted_valuation"),
            "24H Volume": token.get("total_volume"),
        })

    df = pd.DataFrame(output)
    df.to_csv("MEXCData[2].csv", index=False)
    print("✅ Saved to matched_token_data.csv")

if __name__ == "__main__":
    main()
