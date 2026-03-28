from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import requests

from bot.models import WeatherForecast


@dataclass(frozen=True)
class City:
    name: str
    lat: float
    lon: float


MAJOR_US_CITIES: tuple[City, ...] = (
    City("New York", 40.7128, -74.0060),
    City("Los Angeles", 34.0522, -118.2437),
    City("Chicago", 41.8781, -87.6298),
    City("Houston", 29.7604, -95.3698),
    City("Phoenix", 33.4484, -112.0740),
)


def fetch_tomorrow_forecast(base_url: str, city: City) -> WeatherForecast:
    target = dt.date.today() + dt.timedelta(days=1)
    url = f"{base_url}/forecast"
    params = {
        "latitude": city.lat,
        "longitude": city.lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "UTC",
        "forecast_days": 2,
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()

    times = payload["daily"]["time"]
    highs = payload["daily"]["temperature_2m_max"]
    lows = payload["daily"]["temperature_2m_min"]

    target_str = target.isoformat()
    idx = times.index(target_str) if target_str in times else 0

    # Initial uncertainty assumptions in Celsius; calibrate from historical errors.
    high_sigma_c = 2.2
    low_sigma_c = 2.0

    return WeatherForecast(
        city=city.name,
        target_date=target,
        high_c=float(highs[idx]),
        low_c=float(lows[idx]),
        high_sigma_c=high_sigma_c,
        low_sigma_c=low_sigma_c,
    )
