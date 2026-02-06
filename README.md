# SOL Price Aggregator

Production-focused SOL price aggregation tool that pulls spot prices from 20 fixed exchanges (CEX + Solana DEX + P2P) and ranks the cheapest sources in near real-time.

## Features

- 20 mandatory exchanges (10 CEX + 10 Solana DEX)
- P2P cheapest buy rates from 5 marketplaces
- Normalized USD pricing
- Liquidity and slippage checks
- Ranking engine with top-5 cheapest sources
- Auto-refresh with configurable interval

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --once
```

### Options

- `--refresh <seconds>`: refresh interval (default: 15s)
- `--once`: run a single refresh cycle
- `--order-size <usd>`: order size used for DEX slippage checks (default: 1000)

## Notes

- DEX prices are pulled from DexScreener for SOL/USDC pools per exchange.
- Jupiter pricing uses the official Jupiter price endpoint.
- P2P endpoints are public and may rate-limit; the tool retries and caches short-term responses.
