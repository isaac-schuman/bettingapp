from __future__ import annotations

import datetime as dt

from bot.models import MarketContract


class KalshiClient:
    """
    Placeholder Kalshi adapter.

    Replace with authenticated API calls as needed. The method currently returns
    sample contracts to enable end-to-end paper trading tests.
    """

    def list_weather_contracts(self, city: str, target_date: dt.date) -> list[MarketContract]:
        return [
            MarketContract(
                ticker=f"WX-{city[:3].upper()}-{target_date.isoformat()}-HIGH-ABOVE-20C",
                city=city,
                target_date=target_date,
                metric="high",
                threshold_c=20.0,
                yes_price=0.47,
            ),
            MarketContract(
                ticker=f"WX-{city[:3].upper()}-{target_date.isoformat()}-LOW-BELOW-8C",
                city=city,
                target_date=target_date,
                metric="low",
                threshold_c=8.0,
                yes_price=0.43,
            ),
        ]
