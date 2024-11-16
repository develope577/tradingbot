import logging
import time
from config import CloudConfig, TradingConfig
from live_data_fetcher import LiveDataFetcher
from ml_model import MLModel
from strategy import Strategy
from trade_executor import TradeExecutor
import boto3  # Importing boto3 for AWS S3 interaction
import config

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Storage:
    def __init__(self, aws_access_key, aws_secret_key, bucket_name):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket_name = bucket_name

    def save_trade_data(self, symbol, action, confidence):
        """Save trade data to S3"""
        file_name = f"{symbol}_{action}_{int(time.time())}.txt"
        content = f"Action: {action}\nConfidence: {confidence}\nTimestamp: {time.time()}"

        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=content
        )
        logger.info(f"Trade data saved to S3: {file_name}")

class TradingBot:
    def __init__(self, strategy, live_data_fetcher, model, symbols, trade_executor, s3_storage=None):
        self.strategy = strategy
        self.live_data_fetcher = live_data_fetcher
        self.model = model
        self.symbols = symbols
        self.trade_executor = trade_executor
        self.s3_storage = s3_storage

    def trade(self):
        """Main loop for trading"""
        for symbol in self.symbols:
            logger.info(f"Fetching data for {symbol}")
            live_data = self.live_data_fetcher.fetch_data(symbol)

            if live_data:
                action, confidence = self.strategy.evaluate(live_data)
                logger.info(f"Decision for {symbol}: {action} with confidence {confidence}")

                if action != "HOLD":
                    self.execute_trade(symbol, action)

                # Optionally store trade data to S3
                if self.s3_storage:
                    self.s3_storage.save_trade_data(symbol, action, confidence)

    def execute_trade(self, symbol, action):
        """Executes the buy/sell action"""
        if action == "BUY":
            logger.info(f"Executing buy order for {symbol}")
            self.trade_executor.buy(symbol)
        elif action == "SELL":
            logger.info(f"Executing sell order for {symbol}")
            self.trade_executor.sell(symbol)

def run_trading_bot():
    # Initialize the live data fetcher and strategy
    live_data_fetcher = LiveDataFetcher(fetch_top_50=True)  # Fetch top 50 coins dynamically
    strategy = Strategy(model=MLModel())

    # Fetch the top 50 trading pairs dynamically from LiveDataFetcher
    logger.info("Fetching top 50 trading pairs from Binance")
    symbols = live_data_fetcher.coins  # Get the coins directly from the live_data_fetcher

    # Create the trade executor with the API credentials from TradingConfig
    trade_executor = TradeExecutor() # Use the testnet for paper trading

    # Initialize S3 storage if logging is enabled
    s3_storage = S3Storage(
        aws_access_key=CloudConfig.AWS_ACCESS_KEY,
        aws_secret_key=CloudConfig.AWS_SECRET_KEY,
        bucket_name=CloudConfig.S3_BUCKET_NAME
    ) if TradingConfig.LOG_LEVEL != 'OFF' else None

    # Create the trading bot instance
    bot = TradingBot(strategy, live_data_fetcher, model=MLModel(), symbols=symbols, trade_executor=trade_executor,
                     s3_storage=s3_storage)

    # Run the bot indefinitely or for a fixed number of cycles
    while True:
        logger.info("Starting new trading cycle")
        bot.trade()

        # Wait for the next interval (this could be set to match your desired trade interval)
        time.sleep(60 * 15)  # 15-minute interval for each cycle (or whatever is configured in settings.py)

if __name__ == '__main__':
    run_trading_bot()
