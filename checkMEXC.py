import requests
import csv

# Your list of CoinGecko token IDs (shortened here for demo; use your full list in actual code)
coingecko_ids = [
    "de-fi", "defiway", "selfiesteve", "solana-social-explorer", "soroosh-smart-ecosystem",
    "apenft", "fungify-nft-index", "nft-protocol", "catcoin-token", "cats-2", "catscoin-2",
    "goldencat", "ton-cats-jetton", "insect", "inspect", "everipedia", "iq6900", "bonsai3",
    "garden-2", "kalijo", "seed-2", "seed-3", "seed-photo", "nodestats", "suins-token",
    "iris-network", "iris-token-2", "beamswap", "glint-coin", "bionergy", "bio-protocol",
    "agent-doge-by-virtuals", "arbdoge-ai", "solana", "wrapped-solana", "a3s", "alva",
    "astarter", "xena-finance", "xen-crypto", "gelato", "gelato-2", "assangedao",
    "justice-for-pnut-and-fred", "dogebonk", "donablock", "tron", "m-2", "mantis", "memecore",
    "metaverse-m", "monii", "ten-best-coins", "tour-billion-coin", "turingbitchain", "kiki-2",
    "animated", "synthesizeai", "synthr", "synthswap", "litecoin", "localtrade",
    "luxury-travel-token", "jupiter", "jupiter-exchange-solana", "orbit-3", "the-big-grift",
    "avalanche-2", "wrapped-bitcoin", "aura-2", "aura-ai", "aura-finance", "aura-network",
    "decentraland", "streamcoin", "solayer", "unilayer", "ontology", "swell-network",
    "crypto-com-chain", "shiba-wing", "snap-2", "tap-hold-and-load-in-4k", "revox", "rex-3",
    "suirex", "shillguy", "shill-token", "debridge", "dola-borrowing-right", "marine-moguls",
    "mogul-productions-2", "prosper", "wicrypt", "hackenai", "hapticai", "hyzen-ai",
    "let-s-get-hai", "davinci-coin-2", "dogcoin-2", "chromaway", "chronos-finance", "agent-s",
    "sonic-3", "soperme", "token-s", "gateway-to-mars", "mars-2", "mars-3", "marscoin",
    "fact0rn", "orcfax", "libra-4", "libra-5", "king-of-meme", "lion-token", "saturna",
    "super-athletes-token", "defi-yield-protocol", "remme", "pepa-erc", "mantle", "mr-mint",
    "mundoteam", "mynth", "bitci-blok", "bloktopia", "astar", "ripple", "artela-network",
    "exchangeart", "genify-art", "liveart", "salvor", "multichain", "terra-luna", "maga-dog",
    "star-atlas", "the-sandbox", "kekius-maximus", "bware-infra", "cryptogpt-token",
    "spartacus", "sperax", "everid", "space-id", "bitmeme-2", "bytom", "zencash", "zenfrogs",
    "zenith-2", "zenith-3", "meme-trumpcoin", "moontrump", "official-trump", "helichain",
    "heliswap", "one-punch-cat", "punching-cat", "fightly", "swyft-2", "geodnet",
    "aavegotchi-alpha", "alpha-fi", "alpha-finance"
]

# Get token baseAsset list from MEXC
def get_mexc_token_list():
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    response = requests.get(url)
    symbols = response.json().get("symbols", [])
    return set(s["baseAsset"].lower() for s in symbols)

# Filter tokens
def filter_tokens(ids, mexc_tokens):
    return [token_id for token_id in ids if token_id.lower() in mexc_tokens]

# Write matched tokens to CSV
def export_to_csv(token_list, filename="matched_tokens.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Matched_CoinGecko_ID"])
        for token in token_list:
            writer.writerow([token])

# Run filtering and export
mexc_tokens = get_mexc_token_list()
matched = filter_tokens(coingecko_ids, mexc_tokens)
export_to_csv(matched)

print("✅ CSV file created: matched_tokens.csv")
