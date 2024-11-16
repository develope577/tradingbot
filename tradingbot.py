import time
import logging
from strategy import Strategy
from ml_model import MLModel
from trade_executor import TradeExecutor
from live_data_fetcher import LiveDataFetcher
from config import TradingConfig


class TradingBot:
    def __init__(self, strategy, ml_model, trade_executor, live_data_fetcher):
        self.strategy = strategy
        self.model = model
        self.trade_executor = trade_executor
        self.live_data_fetcher = live_data_fetcher
        self.trade_history = []
        self.balance = 1000  # Initial balance for testing

    def run(self):
        """Main loop for trading bot"""
        while True:
            logging.info("Fetching live data...")
            all_live_data = self.live_data_fetcher.fetch_live_data_for_all_coins()

            for symbol, data in all_live_data.items():
                action, confidence = self.strategy.evaluate(data)
                if action == "BUY" and confidence >= BUY_THRESHOLD:
                    logging.info(f"Buying {symbol} with confidence {confidence}")
                    self.trade_executor.execute_buy(symbol, self.balance)
                elif action == "SELL" and confidence >= SELL_THRESHOLD:
                    logging.info(f"Selling {symbol} with confidence {confidence}")
                    self.trade_executor.execute_sell(symbol, self.balance)

            time.sleep(60)  # Sleep for 1 minute before the next cycle


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize the strategy, model, executor, and live data fetcher
    strategy = Strategy(model=MLModel())
    model = MLModel()
    trade_executor = TradeExecutor()
    live_data_fetcher = LiveDataFetcher(fetch_top_50=True)  # Fetch top 50 coins dynamically

    bot = TradingBot(strategy, model, trade_executor, live_data_fetcher)
    bot.run()
