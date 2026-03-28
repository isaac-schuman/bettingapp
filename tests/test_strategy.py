import datetime as dt
import unittest

from bot.models import MarketContract, WeatherForecast
from bot.strategy import fair_yes_probability, find_opportunities, kelly_size


class StrategyTests(unittest.TestCase):
    def test_high_above_threshold_probability(self):
        forecast = WeatherForecast(
            city="Chicago",
            target_date=dt.date(2026, 3, 29),
            high_c=25,
            low_c=10,
            high_sigma_c=2,
            low_sigma_c=2,
        )
        contract = MarketContract(
            ticker="X",
            city="Chicago",
            target_date=forecast.target_date,
            metric="high",
            threshold_c=20,
            yes_price=0.3,
        )
        p = fair_yes_probability(forecast, contract)
        self.assertGreater(p, 0.95)

    def test_find_yes_opportunity(self):
        forecast = WeatherForecast(
            city="NYC",
            target_date=dt.date(2026, 3, 29),
            high_c=22,
            low_c=9,
            high_sigma_c=2,
            low_sigma_c=2,
        )
        c = MarketContract(
            ticker="Y",
            city="NYC",
            target_date=forecast.target_date,
            metric="high",
            threshold_c=20,
            yes_price=0.4,
        )
        opps = find_opportunities(forecast, [c], min_edge=0.1)
        self.assertEqual(len(opps), 1)
        self.assertEqual(opps[0].side, "yes")

    def test_kelly_size_respects_max(self):
        size = kelly_size(
            side="yes",
            fair_yes=0.7,
            market_yes=0.4,
            bankroll=1000,
            kelly_fraction=0.5,
            max_bet_size=30,
        )
        self.assertLessEqual(size, 30)


if __name__ == "__main__":
    unittest.main()
