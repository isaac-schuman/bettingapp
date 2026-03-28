from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    paper_trading: bool = os.getenv("PAPER_TRADING", "true").lower() == "true"
    paper_starting_cash: float = float(os.getenv("PAPER_STARTING_CASH", "1000"))
    max_bet_size: float = float(os.getenv("MAX_BET_SIZE", "25"))
    min_edge: float = float(os.getenv("MIN_EDGE", "0.07"))
    kelly_fraction: float = float(os.getenv("KELLY_FRACTION", "0.2"))
    open_meteo_base_url: str = os.getenv("OPEN_METEO_BASE_URL", "https://api.open-meteo.com/v1")
    kalshi_api_base: str = os.getenv("KALSHI_API_BASE", "https://trading-api.kalshi.com/trade-api/v2")


SETTINGS = Settings()
