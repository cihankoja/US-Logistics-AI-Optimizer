import unittest
from analytics import LogisticsEngine

class TestLogisticsEngine(unittest.TestCase):
    def setUp(self):
        """Initialize the engine before each test"""
        self.engine = LogisticsEngine()

    def test_pricing_logic(self):
        """Test if final price is higher than base price due to mileage and surges"""
        base_price = 50
        distance = 10 # miles
        
        # Calculate metrics
        metrics = self.engine.calculate_metrics(base_price, distance)
        
        # The price should at least be (50 + 10 * 2.25) = 72.5
        self.assertGreaterEqual(metrics['final_price'], 72.5)
        print(f"Pricing Test Passed: ${metrics['final_price']}")

    def test_hazard_impact_on_speed(self):
        """Test if hazard detection correctly affects delivery time (ETA)"""
        distance = 30 # miles
        
        # Case 1: Normal conditions (25 MPH)
        # Time = (30/25)*60 = 72 minutes (without rush hour)
        normal_metrics = self.engine.calculate_metrics(100, distance)
        
        # We check the logic by forcing a hazard check if needed 
        # but here we test the real-time logic from the engine
        if normal_metrics['has_hazard']:
            # If it's currently freezing in NYC, speed should be 15 MPH
            # (30/15)*60 = 120 minutes
            self.assertGreaterEqual(normal_metrics['eta_min'], 120)
            print("Hazard Detected: Safety speed (15 MPH) is active.")
        else:
            # If weather is fine, speed should be 25 MPH
            self.assertLessEqual(normal_metrics['eta_min'], 120)
            print("Clear Weather: Standard speed (25 MPH) is active.")

    def test_data_types(self):
        """Ensure the engine returns correct data types for the dashboard"""
        results = self.engine.calculate_metrics(50, 5)
        self.assertIsInstance(results['final_price'], float)
        self.assertIsInstance(results['eta_min'], float)
        self.assertIsInstance(results['has_hazard'], bool)
        print("Data Type Validation Passed.")

if __name__ == "__main__":
    print("Starting Unit Tests for NYC Logistics Engine...\n")
    unittest.main()