import logging
import time
import talib
import requests
import numpy as np
from config import TradingConfig, ModelConfig
from binance.client import Client  # Binance client for API access

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LiveDataFetcher:
    def __init__(self, fetch_top_50=True):
        self.fetch_top_50 = fetch_top_50
        # Fetch the top 50 coins dynamically from Binance
        self.coins = self.get_top_50_coins() if fetch_top_50 else []

    def get_top_50_coins(self):
        """Fetches the top 50 coins dynamically from Binance"""
        # Initialize Binance client (ensure to set your API keys in the TradingConfig)
        client = Client(api_key=TradingConfig.API_KEY, api_secret=TradingConfig.API_SECRET)

        # Fetch market data (tickers) from Binance API
        tickers = client.get_ticker()  # Fetch all market data (tickers) from Binance

        # Sort tickers by trading volume (quoteVolume) and select top 50
        top_50 = sorted(tickers, key=lambda x: float(x['quoteVolume']), reverse=True)[:50]

        # Extract the symbol names from the top 50 sorted tickers
        top_50_symbols = [ticker['symbol'] for ticker in top_50]

        return top_50_symbols

    def fetch_data(self, symbol):
        """ Fetch live data from Binance API for a symbol """
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100'
        response = requests.get(url)
        data = response.json()

        # Extract OHLC data
        ohlc_data = []
        for entry in data:
            ohlc_data.append({
                'timestamp': entry[0],
                'open': float(entry[1]),
                'high': float(entry[2]),
                'low': float(entry[3]),
                'close': float(entry[4]),
                'volume': float(entry[5])
            })

        # Calculate additional features (e.g., RSI, MACD)
        close_prices = [entry['close'] for entry in ohlc_data]
        rsi = talib.RSI(np.array(close_prices), timeperiod=14)
        macd, signal, _ = talib.MACD(np.array(close_prices), fastperiod=12, slowperiod=26, signalperiod=9)
        ema = talib.EMA(np.array(close_prices), timeperiod=9)

        # Prepare features (e.g., volume, MACD, RSI, EMA)
        features = {
            'rsi': rsi[-1],  # Last RSI value
            'macd': macd[-1],  # Last MACD value
            'signal': signal[-1],  # Last Signal Line value
            'ema': ema[-1],  # Last EMA value
            'volume': ohlc_data[-1]['volume'],  # Latest volume
            'timestamp': ohlc_data[-1]['timestamp']  # Timestamp for the data
        }

        return features

    def fetch_live_data_for_all_coins(self):
        """ Fetch live data for all coins in the list """
        all_data = {}
        for coin in self.coins:
            all_data[coin] = self.fetch_data(coin)
        return all_data
