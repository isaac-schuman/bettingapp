from __future__ import annotations

import argparse
import logging
import time

from bot.config import SETTINGS
from bot.kalshi import KalshiClient
from bot.paper import PaperPortfolio
from bot.strategy import find_opportunities, kelly_size
from bot.weather import MAJOR_US_CITIES, fetch_tomorrow_forecast


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def run_once(portfolio: PaperPortfolio, kalshi: KalshiClient) -> None:
    for city in MAJOR_US_CITIES:
        forecast = fetch_tomorrow_forecast(SETTINGS.open_meteo_base_url, city)
        contracts = kalshi.list_weather_contracts(city.name, forecast.target_date)
        opps = find_opportunities(forecast, contracts, SETTINGS.min_edge)

        for opp in opps[:2]:
            size_usd = kelly_size(
                side=opp.side,
                fair_yes=opp.fair_yes,
                market_yes=opp.contract.yes_price,
                bankroll=portfolio.cash,
                kelly_fraction=SETTINGS.kelly_fraction,
                max_bet_size=SETTINGS.max_bet_size,
            )
            qty = int(size_usd)
            trade_price = opp.contract.yes_price if opp.side == "yes" else (1.0 - opp.contract.yes_price)
            fill = portfolio.place_order(opp.contract.ticker, opp.side, trade_price, qty)
            if fill:
                logger.info(
                    "Filled paper order city=%s ticker=%s side=%s qty=%s price=%.3f edge=%.3f cash=%.2f",
                    city.name,
                    fill.ticker,
                    fill.side,
                    fill.qty,
                    fill.price,
                    opp.edge_selected,
                    portfolio.cash,
                )


def main() -> None:
    parser = argparse.ArgumentParser(description="Kalshi weather mispricing scanner")
    parser.add_argument("--once", action="store_true", help="Run one scan cycle and exit")
    parser.add_argument("--loop", action="store_true", help="Run forever")
    parser.add_argument("--interval-seconds", type=int, default=900)
    args = parser.parse_args()

    portfolio = PaperPortfolio(cash=SETTINGS.paper_starting_cash)
    kalshi = KalshiClient()

    if args.once or not args.loop:
        run_once(portfolio, kalshi)
        return

    while True:
        run_once(portfolio, kalshi)
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    main()
