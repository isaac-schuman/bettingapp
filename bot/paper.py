from __future__ import annotations

from dataclasses import dataclass, field

from bot.models import Fill, Position


@dataclass
class PaperPortfolio:
    cash: float
    positions: dict[str, Position] = field(default_factory=dict)
    fills: list[Fill] = field(default_factory=list)

    def place_order(self, ticker: str, side: str, price: float, qty: int) -> Fill | None:
        if qty <= 0:
            return None

        cost = price * qty
        if cost > self.cash:
            qty = int(self.cash // max(price, 1e-9))
            if qty <= 0:
                return None
            cost = price * qty

        self.cash -= cost
        fill = Fill(ticker=ticker, side=side, price=price, qty=qty)
        self.fills.append(fill)

        if ticker not in self.positions:
            self.positions[ticker] = Position(ticker=ticker, side=side, avg_price=price, qty=qty)
        else:
            pos = self.positions[ticker]
            new_qty = pos.qty + qty
            new_avg = (pos.avg_price * pos.qty + price * qty) / new_qty
            self.positions[ticker] = Position(ticker=ticker, side=side, avg_price=new_avg, qty=new_qty)

        return fill
