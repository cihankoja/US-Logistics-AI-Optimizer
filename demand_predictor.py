import statistics

class DeliveryAI:
    """Predicts future delivery trends based on historical price data."""
    
    def __init__(self, price_history):
        # AI models thrive on data; we store history to find patterns
        self.history = price_history

    def predict_next_price_trend(self):
        """Simple moving average to predict the next price point."""
        if len(self.history) < 3:
            return "Collecting more data for AI prediction..."
        
        # Taking the average of the last 3 orders to predict the next one
        prediction = statistics.mean(self.history[-3:])
        return f"${round(prediction, 2)}"

    def get_market_volatility(self):
        """Calculates standard deviation to measure market stability."""
        if len(self.history) < 2:
            return 0.0
        return round(statistics.stdev(self.history), 2)