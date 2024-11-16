import pandas as pd
import numpy as np

class DataProcessor:
    def process_data(self, raw_data):
        """Process raw market data into features for the model"""
        df = pd.DataFrame(raw_data)
        # Process and prepare data (example)
        df['macd_signal'] = df['macd'] - df['signal']
        df['rsi'] = df['rsi']
        df['ema'] = df['ema']
        df['volume'] = df['volume']
        # Example processing, this could be expanded based on needs
        return df
