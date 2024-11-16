from config import TradingConfig
from binance.client import Client  # Import the Binance client

import config

class TradeExecutor:
    def __init__(self):
        # Directly provide API keys for Testnet
        self.client = Client(api_key='xrYFJ29Wpolc3dRaS6YeZwTV0Cv5QIzdK8o5xSvmkEfJVMA2JEnSBkHILSoUbhxL', api_secret='GwfRsE23B1ATS7LdBMmGkSOw1aLuOVHVoiwYm4X3Scsk27mBJcIOcdCASmQrprvj', testnet=True)


    def get_trade_quantity(self, coin):
        """Calculate quantity based on TRADE_BUDGET_USD and coin price."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=coin)  # Get live price
            price = float(ticker['price'])  # Current price of the coin
            quantity = TradingConfig.TRADE_BUDGET_USD / price  # Calculate quantity
            return round(quantity, 6)  # Binance supports up to 6 decimal places
        except Exception as e:
            print(f"Error fetching price for {coin}: {e}")
            return None

    def execute_buy(self, coin):
        """Execute a buy order."""
        quantity = self.get_trade_quantity(coin)  # Get calculated quantity
        if not quantity:
            return None
        try:
            order = self.client.order_market_buy(
                symbol=coin,
                quantity=quantity
            )
            print(f"Bought {quantity} of {coin}")
            return order
        except Exception as e:
            print(f"Error executing buy for {coin}: {e}")

    def execute_sell(self, coin):
        """Execute a sell order."""
        # For simplicity, we'll use the same logic for calculating quantity.
        quantity = self.get_trade_quantity(coin)  # Get calculated quantity
        if not quantity:
            return None
        try:
            order = self.client.order_market_sell(
                symbol=coin,
                quantity=quantity
            )
            print(f"Sold {quantity} of {coin}")
            return order
        except Exception as e:
            print(f"Error executing sell for {coin}: {e}")
