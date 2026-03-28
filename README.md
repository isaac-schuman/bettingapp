# Kalshi Weather Mispricing Bot (Paper Trading First)

This repository contains a starter bot framework for identifying potential mispricings in daily weather markets (highs/lows in major cities), paper trading those opportunities, and running continuously in the background.

## What this does

- Pulls **weather forecasts** from Open-Meteo.
- Ingests **market contracts** from a Kalshi-style client interface.
- Estimates fair probabilities for threshold contracts (e.g. `HIGH_TEMP_ABOVE_75`).
- Computes edge between model fair value and market implied probability.
- Places paper trades with configurable risk and max bet size.
- Logs positions, fills, and PnL snapshots.

## Safety / rollout plan

1. **Paper trade only** for at least 2-4 weeks.
2. Track calibration by city/lead-time to verify edge quality.
3. Go live with very small limits (e.g. $5-$10 per contract).
4. Add hard stop-loss and max daily loss limits before scaling.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m bot.main --once
```

## Run continuously

```bash
python -m bot.main --loop --interval-seconds 900
```

Use a process manager like `systemd`, `supervisord`, or Docker restart policies for always-on operation.

## Notes

- Default mode is **paper trading** (`PAPER_TRADING=true`).
- Kalshi integration here is intentionally lightweight and can be replaced with authenticated endpoints in `bot/kalshi.py`.
- This code is educational scaffolding and not financial advice.
