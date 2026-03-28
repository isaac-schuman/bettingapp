from __future__ import annotations

import math

from bot.models import MarketContract, Opportunity, WeatherForecast


def normal_cdf(x: float, mu: float, sigma: float) -> float:
    z = (x - mu) / (sigma * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


def fair_yes_probability(forecast: WeatherForecast, contract: MarketContract) -> float:
    if contract.metric == "high":
        mu = forecast.high_c
        sigma = forecast.high_sigma_c
        # P(high > threshold)
        return max(0.0, min(1.0, 1.0 - normal_cdf(contract.threshold_c, mu, sigma)))

    if contract.metric == "low":
        mu = forecast.low_c
        sigma = forecast.low_sigma_c
        # P(low < threshold)
        return max(0.0, min(1.0, normal_cdf(contract.threshold_c, mu, sigma)))

    raise ValueError(f"Unsupported metric: {contract.metric}")


def find_opportunities(
    forecast: WeatherForecast,
    contracts: list[MarketContract],
    min_edge: float,
) -> list[Opportunity]:
    opportunities: list[Opportunity] = []
    for contract in contracts:
        fair_yes = fair_yes_probability(forecast, contract)
        edge_yes = fair_yes - contract.yes_price
        edge_no = (1.0 - fair_yes) - (1.0 - contract.yes_price)

        if edge_yes >= min_edge:
            opportunities.append(
                Opportunity(
                    contract=contract,
                    fair_yes=fair_yes,
                    edge_yes=edge_yes,
                    side="yes",
                    edge_selected=edge_yes,
                )
            )
        elif edge_no >= min_edge:
            opportunities.append(
                Opportunity(
                    contract=contract,
                    fair_yes=fair_yes,
                    edge_yes=edge_yes,
                    side="no",
                    edge_selected=edge_no,
                )
            )

    return sorted(opportunities, key=lambda o: o.edge_selected, reverse=True)


def kelly_size(
    side: str,
    fair_yes: float,
    market_yes: float,
    bankroll: float,
    kelly_fraction: float,
    max_bet_size: float,
) -> float:
    p = fair_yes if side == "yes" else (1.0 - fair_yes)
    q = 1.0 - p
    price = market_yes if side == "yes" else (1.0 - market_yes)

    if price <= 0.0 or price >= 1.0:
        return 0.0

    b = (1.0 - price) / price
    raw_fraction = (b * p - q) / b
    fraction = max(0.0, raw_fraction) * max(0.0, min(1.0, kelly_fraction))
    size = bankroll * fraction
    return max(0.0, min(size, max_bet_size))
