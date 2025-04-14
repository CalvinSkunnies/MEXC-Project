import requests
import time
import csv

def get_all_mexc_token_symbols():
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    all_tokens = set()

    headers = {
        "User-Agent": "Chrome/5.0",  # Helps avoid connection issues
        # "X-MEXC-APIKEY": "mx0vglMdf1KwfydbVr"  # Optional if required in future
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(0.75)
        response.raise_for_status()
        data = response.json()
        symbols = data.get("symbols", [])

        for symbol in symbols:
            base_asset = symbol.get("baseAsset")
            if base_asset:
                all_tokens.add(base_asset)

        token_list = sorted(all_tokens)
        print(f"✅ Total unique tokens on MEXC: {len(token_list)}\n")

        # Save to CSV
        with open("MEXCTokens.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Token"])  # Header
            for token in token_list:
                writer.writerow([token])

        print("💾 Tokens saved to MEXCTokens.csv")
        return token_list

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return []

if __name__ == "__main__":
    tokens = get_all_mexc_token_symbols()
    for token in tokens:
        print(token)
