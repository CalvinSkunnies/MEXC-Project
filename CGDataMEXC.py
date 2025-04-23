import requests
import pandas as pd
import time
import math

API_KEY = "CG-MfMJsvzUhR8PtJfvvSRi1UEm"
COINGECKO_URL = "https://pro-api.coingecko.com/api/v3"
HEADERS = {"x_cg_pro_api_key": API_KEY}

# Load your list of coin IDs
def load_token_ids(file_path):
    df = pd.read_csv(file_path)
    return df["Coin ID"].dropna().tolist()

# Fetch market data in batches of 250
def fetch_market_data(coin_ids):
    all_data = []
    batch_size = 250
    total_batches = math.ceil(len(coin_ids) / batch_size)

    for i in range(total_batches):
        batch = coin_ids[i * batch_size:(i + 1) * batch_size]
        ids = ",".join(batch)

        url = f"{COINGECKO_URL}/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ids,
            "price_change_percentage": "24h",
        }

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            batch_data = response.json()

            for token in batch_data:
                all_data.append({
                    "ID": token.get("id"),
                    "Name": token.get("name"),
                    "Symbol": token.get("symbol"),
                    "Market Cap": token.get("market_cap"),
                    "FDV": token.get("fully_diluted_valuation"),
                    "24H Volume": token.get("total_volume"),
                })

            print(f"✅ Batch {i+1}/{total_batches} fetched.")
        except Exception as e:
            print(f"❌ Error on batch {i+1}: {e}")
        
        time.sleep(1)  # avoid hitting rate limits

    return all_data

# Main script
def main():
    token_ids = load_token_ids("MEXCData.csv")  # Replace with your CSV file
    market_data = fetch_market_data(token_ids)

    df = pd.DataFrame(market_data)
    df.to_csv("MEXCData[2].csv", index=False)
    print("✅ All done. Data saved to MEXCData[2].csv")

if __name__ == "__main__":
    main()
