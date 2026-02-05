import unittest
from demand_predictor import DeliveryAI

class TestAI(unittest.TestCase):
    def test_prediction_logic(self):
        prices = [10.0, 20.0, 30.0]
        ai = DeliveryAI(prices)
        # (10+20+30) / 3 = 20.0
        self.assertEqual(ai.predict_next_price_trend(), "$20.0")

if __name__ == "__main__":
    unittest.main()