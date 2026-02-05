import requests
import matplotlib.pyplot as plt
from datetime import datetime
import json

class LogisticsEngine:
    def __init__(self):
        self.lat, self.lon = 40.71, -74.00
        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current_weather=True"

    def get_weather_data(self):
        try:
            response = requests.get(self.api_url).json()
            curr = response['current_weather']
            temp_f = (curr['temperature'] * 9/5) + 32
            return temp_f, curr['weathercode']
        except:
            return 30.0, 71 

    def calculate_metrics(self, base_price, distance_miles):
        temp_f, w_code = self.get_weather_data()
        current_hour = datetime.now().hour
        is_rush = (8 <= current_hour <= 10) or (16 <= current_hour <= 19)
        
        is_freezing = temp_f <= 32
        has_hazard = is_freezing or w_code > 60

        ## SPEED AND ETA LOGIC
        current_speed = 15 if has_hazard else 25
        base_time_min = (distance_miles / current_speed) * 60
        traffic_impact = 1.6 if is_rush else 1.0
        final_eta = base_time_min * traffic_impact
        
        ## SURGE PRICING LOGIC
        traffic_mult = 1.35 if is_rush else 1.0
        weather_mult = 1.40 if has_hazard else 1.0
        final_price = (base_price + (distance_miles * 2.25)) * traffic_mult * weather_mult
        
        return {
            "final_price": round(final_price, 2),
            "eta_min": round(final_eta, 1),
            "temp_f": round(temp_f, 1),
            "is_rush": is_rush,
            "has_hazard": has_hazard
        }

    def generate_dashboard(self, orders):
        route_labels = [f"ID: {o['driver_id']}\n({o['distance_miles']} mi)" for o in orders]
        results = [self.calculate_metrics(o['base_price'], o['distance_miles']) for o in orders]
        
        final_prices = [r['final_price'] for r in results]
        etas = [r['eta_min'] for r in results]
        temp_f = results[0]['temp_f']
        is_rush = results[0]['is_rush']
        has_hazard = results[0]['has_hazard']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        orange_color = '#e67e22'
        blue_color = '#2980b9'
        hazard_red = '#c0392b'

        ## HEADER WITH DYNAMIC COLOR ONLY FOR TEXT
        title_text = f"NYC LOGISTICS OPERATIONAL DASHBOARD | Temp: {temp_f}°F"
        if has_hazard:
            title_text += "\n WARNING: FREEZING CONDITIONS - ICY ROADS DETECTED "
        
        fig.suptitle(title_text, fontsize=16, fontweight='bold', color=hazard_red if has_hazard else '#2c3e50')

        ## CHART 1: ETA ANALYSIS
        ax1.barh(route_labels, etas, color=orange_color, alpha=0.85)
        ax1.set_title("Safety-Adjusted ETA (Minutes)", fontsize=12, fontweight='bold')
        ax1.set_xlabel("Minutes to Destination")
        ax1.grid(axis='x', linestyle='--', alpha=0.5)

        ## CHART 2: PRICING ANALYSIS
        ax2.bar(route_labels, final_prices, color=blue_color, alpha=0.85)
        ax2.set_title("Hazard-Adjusted Dynamic Pricing (USD)", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Total Price ($)")
        ax2.grid(axis='y', linestyle='--', alpha=0.5)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig('logistics_dashboard.png')
        print(f"Dashboard generated successfully.")

if __name__ == "__main__":
    with open('orders.json', 'r') as f:
        data = json.load(f)
    LogisticsEngine().generate_dashboard(data)