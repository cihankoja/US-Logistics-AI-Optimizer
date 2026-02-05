import requests
import matplotlib.pyplot as plt

class WeatherService:
    @staticmethod
    def get_weather_multiplier(city="New York"):
        # New York city coordinates
        lat, lon = 40.71, -74.00 
        
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
            response = requests.get(url).json()
            curr = response['current_weather']
            
            temp_c = curr['temperature']
            # convert to Fahrenheit
            temp_f = (temp_c * 9/5) + 32
            w_code = curr['weathercode']
            
            impact_map = {
                0:  (1.00, "Clear Sky"),
                1:  (1.02, "Mainly Clear"),
                2:  (1.05, "Partly Cloudy"),
                3:  (1.08, "Overcast"),
                45: (1.15, "Foggy (Slow Traffic)"),
                51: (1.12, "Light Drizzle"),
                61: (1.20, "Rainy (High Demand)"),
                71: (1.35, "Snowy (Critical Delay)"),
                95: (1.50, "Thunderstorm (Hazardous)")
            }
            
            multiplier, desc = impact_map.get(w_code, (1.10, "Unstable Weather"))
            
            if temp_f < 32:
                multiplier += 0.05
                desc += " & Freezing Cold"
                
            return {
                "city": city,
                "multiplier": round(multiplier, 2),
                "description": desc,
                "temp_f": round(temp_f, 1)
            }
        except Exception as e:
            return {"multiplier": 1.0, "description": "Offline Mode", "temp_f": "N/A", "city": city}
# Example usage
def save_price_trend(prices):
    plt.figure(figsize=(10, 6))
    plt.plot(prices, marker='o', linestyle='-', color='b')
    plt.title('US Market Delivery Price Analysis')
    plt.xlabel('Order Sequence')
    plt.ylabel('Price in USD')
    plt.grid(True)
    plt.savefig('price_trend.png')
    print("Graph saved as 'price_trend.png'")