import unittest
from src.backend.calculations import calculate_profit_loss, calculate_margin, calculate_risk_reward

class TestCalculations(unittest.TestCase):
    def test_calculate_profit_loss_buy(self):
        profit, loss = calculate_profit_loss(100, 90, 110, 1, "buy")
        self.assertEqual(profit, 10)
        self.assertEqual(loss, 10)

    def test_calculate_profit_loss_sell(self):
        profit, loss = calculate_profit_loss(100, 110, 90, 1, "sell")
        self.assertEqual(profit, 10)
        self.assertEqual(loss, 10)

    def test_calculate_margin(self):
        margin = calculate_margin(100, 1)
        self.assertEqual(margin, 2)

    def test_calculate_risk_reward(self):
        risk_reward = calculate_risk_reward(10, 5)
        self.assertEqual(risk_reward, 2)

if __name__ == '__main__':
    unittest.main()
