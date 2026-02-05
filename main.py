import json
import logging
import os
from analytics import save_price_trend, WeatherService
from demand_predictor import DeliveryAI  

# Log configuration
logging.basicConfig(filename='system_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class USDeliveryOptimizer:
    def __init__(self):
        self.base_fare = 5.99
        self.mileage_rate = 1.50
        self.calculated_prices = [] # Store for AI analysis

    def calculate_surge_price(self, distance, is_rush_hour, w_mult):
        try:
            price = self.base_fare + (distance * self.mileage_rate)
            price *= w_mult
            
            if is_rush_hour:
                price += 4.50
                
            final_price = round(price, 2)
            self.calculated_prices.append(final_price) # Feed the data list
            return final_price
        except Exception as e:
            logging.error(f"Calculation error: {e}")
            return None

    def process_batch(self, file_path, w_mult):
        with open(file_path, 'r') as file:
            orders = json.load(file)
            print(f"{'ID':<5} | {'Customer':<12} | {'Price':<8} | {'Status'}")
            print("-" * 50)
            for o in orders:
                p = self.calculate_surge_price(o['distance_miles'], o['is_rush_hour'], w_mult)
                print(f"{o['order_id']:<5} | {o['customer']:<12} | ${p:<7} | NY Adjusted")
                
if __name__ == "__main__":
    weather_data = WeatherService.get_weather_multiplier()
    w_mult = weather_data['multiplier']
    print(f"--- NY LIVE LOGISTICS REPORT ---")
    print(f"Current Condition: {weather_data['description']}")
    print(f"Temperature: {weather_data['temp_f']}°F")
    print(f"Surge Multiplier: x{w_mult}")
    print("-" * 50)

    optimizer = USDeliveryOptimizer()
    
    # 1. Process existing orders
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "orders.json")
    optimizer.process_batch(file_path, w_mult)
    
    # 2. Trigger AI Prediction
    print("\n--- AI Market Insights ---")
    ai_engine = DeliveryAI(optimizer.calculated_prices)
    print(f"Predicted Price for Next Order: {ai_engine.predict_next_price_trend()}")
    print(f"Market Volatility Index: {ai_engine.get_market_volatility()}")
    
    logging.info("Batch processing and AI prediction completed successfully.")
    save_price_trend(optimizer.calculated_prices)