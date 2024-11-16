import requests

def get_top_50_coins():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()

    # Sorting by volume, get top 50 coins
    top_50 = sorted(data, key=lambda x: float(x['quoteVolume']), reverse=True)[:50]
    return [coin['symbol'] for coin in top_50]
