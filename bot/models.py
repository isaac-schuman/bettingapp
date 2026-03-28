from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class WeatherForecast:
    city: str
    target_date: date
    high_c: float
    low_c: float
    high_sigma_c: float
    low_sigma_c: float


@dataclass(frozen=True)
class MarketContract:
    ticker: str
    city: str
    target_date: date
    metric: str  # "high" or "low"
    threshold_c: float
    yes_price: float  # in [0, 1]


@dataclass(frozen=True)
class Opportunity:
    contract: MarketContract
    fair_yes: float
    edge_yes: float
    side: str  # "yes" or "no"
    edge_selected: float


@dataclass
class Fill:
    ticker: str
    side: str
    price: float
    qty: int


@dataclass
class Position:
    ticker: str
    side: str
    avg_price: float
    qty: int
