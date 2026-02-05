import unittest
from main import USDeliveryOptimizer

class TestUSDeliveryOptimizer(unittest.TestCase):
    def setUp(self):
        """Before every test, create an instance of the optimizer."""
        self.optimizer = USDeliveryOptimizer()

    def test_clear_weather_calculation(self):
        # 3.2 miles, Clear weather, Rush hour = ($5.99 + (3.2 * 1.5)) * 1.0 + 4.5 = $15.29
        result = self.optimizer.calculate_surge_price(3.2, "Clear", True)
        self.assertEqual(result, 15.29)

    def test_heavy_rain_calculation(self):
        # 8.5 miles, Heavy Rain, No Rush Hour = ($5.99 + (8.5 * 1.5)) * 1.4 = $26.24
        result = self.optimizer.calculate_surge_price(8.5, "Heavy Rain", False)
        self.assertEqual(result, 26.24)

    def test_invalid_weather(self):
        # unkown weather type should default to 1.0 multiplier
        # 2.0 miles, Mysterious Fog, No Rush Hour = ($5.99 + (2.0 * 1.5)) * 1.0 = $8.99
        result = self.optimizer.calculate_surge_price(2.0, "Mysterious Fog", False)
        expected = round(5.99 + (2.0 * 1.5), 2)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()