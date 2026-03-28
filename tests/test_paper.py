import unittest

from bot.paper import PaperPortfolio


class PaperPortfolioTests(unittest.TestCase):
    def test_place_order_reduces_cash(self):
        p = PaperPortfolio(cash=100)
        fill = p.place_order("ABC", "yes", 0.5, 10)
        self.assertIsNotNone(fill)
        self.assertEqual(p.cash, 95)
        self.assertEqual(p.positions["ABC"].qty, 10)

    def test_order_clamped_by_cash(self):
        p = PaperPortfolio(cash=5)
        fill = p.place_order("ABC", "yes", 2.0, 10)
        self.assertIsNotNone(fill)
        self.assertEqual(fill.qty, 2)
        self.assertEqual(p.cash, 1)


if __name__ == "__main__":
    unittest.main()
