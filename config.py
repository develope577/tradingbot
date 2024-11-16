class TradingConfig:
    # --- API Credentials ---
    API_KEY = 'xrYFJ29Wpolc3dRaS6YeZwTV0Cv5QIzdK8o5xSvmkEfJVMA2JEnSBkHILSoUbhxL'
    API_SECRET = 'GwfRsE23B1ATS7LdBMmGkSOw1aLuOVHVoiwYm4X3Scsk27mBJcIOcdCASmQrprvj'

    # --- Coin List ---
    COINS = []  

    # --- Trading Parameters ---
    TRADE_BUDGET_USD = 100  # Fixed amount to trade per coin (in USD)
    TRADING_SYMBOL = ''
    TRADE_INTERVAL = '1hr'
    INITIAL_BALANCE = 10000
    BUY_THRESHOLD = 0.85
    SELL_THRESHOLD = 0.80
    STOP_LOSS = 0.05

    # --- Cloud and Storage Settings ---
    MODEL_SAVE_PATH = 's3://tradingbot577/models/saved_models/'
    LOG_PATH = 's3://tradingbot577/logs/trade_logs.csv'
    CLOUD_BUCKET_NAME = 'tradingbot577'
    CLOUD_SAVE_PATH = 'models/'

    # --- Logging Configuration ---
    LOG_LEVEL = 'INFO'

class CloudConfig:
    # --- Cloud Provider Configuration (Example for AWS S3) ---
    CLOUD_PROVIDER = 'AWS'
    AWS_ACCESS_KEY = 'AKIA5V6I7GVE2JESXAHH'
    AWS_SECRET_KEY = '0S3qgkovYoVSYjpxF2SLDEzAvHZmkePLn2K7mhYB'
    AWS_REGION = 'eu-north-1'
    S3_BUCKET_NAME = 'tradingbot577'

    # --- Storage Paths ---
    MODEL_CLOUD_PATH = 'trading_bot/models/'
    LOG_CLOUD_PATH = 'trading_bot/logs/'
    LIVE_DATA_CLOUD_PATH = 'trading_bot/live_data/'

    # --- Cloud Sync Settings ---
    SYNC_INTERVAL = 60 * 10

class HyperparameterConfig:
    # Hyperparameters for RandomForest
    RANDOM_FOREST_PARAMS = {
        'n_estimators': [50, 100, 150],
        'max_depth': [10, 15, 20],
        'min_samples_split': [5, 10, 20]
    }

    # Hyperparameters for DQN Model
    DQN_PARAMS = {
        'learning_rate': [0.001, 0.0001],
        'gamma': [0.99, 0.95],
        'batch_size': [32, 64]
    }

    # Tracking experiment setup
    EXPERIMENT_NAME = "momentum_trading_experiment"

class ModelConfig:
    # --- ML Model Parameters ---
    ML_MODEL_TYPE = 'RandomForest'
    ML_TRAINING_RATIO = 0.8
    HYPERPARAMETERS = {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5
    }

    # --- Reinforcement Learning Parameters ---
    RL_ALGORITHM = 'DQN'
    DISCOUNT_FACTOR = 0.95
    LEARNING_RATE = 0.001
    EXPLORATION_DECAY = 0.995

    # --- Feature Engineering ---
    FEATURES = [
        'price_change_percentage',
        'macd',
        'rsi',
        'volume',
        'ema'
    ]

    # --- Model Save and Load Settings ---
    AUTO_SAVE_MODEL = True
    MODEL_SAVE_INTERVAL = 10