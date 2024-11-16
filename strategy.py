class Strategy:
    def __init__(self, model=None):
        self.model = model

    def evaluate(self, live_data):
        """
        Evaluates whether to buy or sell based on the strategy
        Parameters:
            live_data (dict): The most recent market data for a coin.
        Returns:
            tuple: (action, confidence) where:
                - action: "BUY", "SELL", or "HOLD"
                - confidence: confidence score of the prediction (e.g., between 0 and 1)
        """
        # Placeholder logic for decision making
        macd, macd_signal = live_data['macd'], live_data['signal']
        volume = live_data['volume']

        confidence = 0.85  # Assume a high-confidence prediction for this example

        if macd > macd_signal and volume > 1000:  # Example logic for buy signal
            return "BUY", confidence
        elif macd < macd_signal:  # Example logic for sell signal
            return "SELL", confidence
        return "HOLD", confidence
