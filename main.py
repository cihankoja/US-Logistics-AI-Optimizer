import json
from analytics import LogisticsEngine

def start_application():
    ## SYSTEM LOG: INITIALIZING THE ENGINE
    print("--- NYC SMART LOGISTICS ENGINE v3.2 ---")
    
    ## LOADING ORDER DATA FROM JSON FILE
    try:
        with open('orders.json', 'r') as f:
            orders = json.load(f)
        print(f"## {len(orders)} orders loaded successfully.")
    except Exception as e:
        print(f"## Error loading JSON: {e}")
        return

    ## INITIALIZING THE ANALYTICS ENGINE AND GENERATING THE VISUALS
    engine = LogisticsEngine()
    print("## Calculating weather & traffic multipliers...")
    
    ## THIS CALLS THE ANALYTICS LOGIC AND CREATES THE DASHBOARD IMAGE
    engine.generate_dashboard(orders)
    
    print("--- PROCESS COMPLETE | Visuals saved to logistics_dashboard.png ---")

if __name__ == "__main__":
    start_application()