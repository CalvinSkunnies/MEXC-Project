import requests
import pandas as pd
import time

# ✅ CoinGecko Pro API Key
API_KEY = "######"
BASE_URL = "https://pro-api.coingecko.com/api/v3"

# Load token names from CSV
def load_tokens(file_path):
    df = pd.read_csv(file_path)
    return df["Token Name"].dropna().tolist()

# Fetch all CoinGecko coins list
def get_all_coins_list():
    url = f"{BASE_URL}/coins/list?x_cg_pro_api_key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Match input tokens to CoinGecko IDs
def match_token_ids(token_list, all_coins):
    matched = {}
    unmatched = []

    for token in token_list:
        token_lower = token.lower()
        match = next(
            (coin for coin in all_coins if coin["symbol"] == token_lower or coin["name"].lower() == token_lower),
            None
        )
        if match:
            matched[token] = match["id"]
        else:
            unmatched.append(token)

    return matched, unmatched

# Fetch market data from CoinGecko (batch)
def fetch_market_data(matched_ids):
    ids_list = list(matched_ids.values())
    output = []

    for i in range(0, len(ids_list), 250):  # Max 250 per call
        batch_ids = ids_list[i:i+250]
        ids_param = ",".join(batch_ids)
        url = f"{BASE_URL}/coins/markets?vs_currency=usd&ids={ids_param}&x_cg_pro_api_key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        output.extend(data)
        time.sleep(1.2)

    return output

# Fetch coin categories using your preferred format
def get_coin_categories(coin_id):
    url = f"{BASE_URL}/coins/{coin_id}?x_cg_pro_api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return ', '.join(data.get("categories", []))
    except Exception as e:
        print(f"Error fetching categories for {coin_id}: {e}")
        return "Unknown"

# Main script
def main():
    input_file = "MEXCData.csv"
    token_list = load_tokens(input_file)

    print("🔍 Fetching all tokens from CoinGecko...")
    all_coins = get_all_coins_list()

    print("🔗 Matching tokens...")
    matched, unmatched = match_token_ids(token_list, all_coins)
    print(f"✅ Matched: {len(matched)} | ❌ Unmatched: {unmatched}")

    print("📊 Fetching market data...")
    data = fetch_market_data(matched)

    output = []
    for token in data:
        category = get_coin_categories(token["id"])
        output.append({
            "Input Token": [k for k, v in matched.items() if v == token["id"]][0],
            "CoinGecko ID": token["id"],
            "Name": token["name"],
            "Symbol": token["symbol"].upper(),
            "Market Cap": token.get("market_cap"),
            "FDV": token.get("fully_diluted_valuation"),
            "24H Volume": token.get("total_volume"),
            "Categories": category,
        })

    df = pd.DataFrame(output)
    df.to_csv("MEXCData2.csv", index=False)
    print("✅ Saved to MEXCData2.csv")

if __name__ == "__main__":
    main()
