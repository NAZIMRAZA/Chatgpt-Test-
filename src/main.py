from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
from typing import List

from src.adapters.cex import (
    BinanceAdapter,
    BitgetAdapter,
    BybitAdapter,
    CoinbaseAdapter,
    GateAdapter,
    HtxAdapter,
    KuCoinAdapter,
    MexcAdapter,
    OkxAdapter,
    UpbitAdapter,
)
from src.adapters.dex import build_dex_adapters
from src.adapters.p2p import build_p2p_adapters
from src.config import CEX_EXCHANGES, DEX_EXCHANGES, DEFAULT_ORDER_SIZE_USD, DEFAULT_REFRESH_SECONDS
from src.display import render_p2p, render_quotes, render_summary, render_top5
from src.http import HttpClient
from src.models import P2POffer, PriceQuote
from src.normalizer import apply_staleness
from src.ranking import build_ranking_result
from src.solana_rpc import SolanaRpc


def build_cex_adapters() -> list:
    return [
        BinanceAdapter("binance"),
        GateAdapter("gate"),
        BybitAdapter("bybit"),
        OkxAdapter("okx"),
        BitgetAdapter("bitget"),
        CoinbaseAdapter("coinbase"),
        UpbitAdapter("upbit"),
        KuCoinAdapter("kucoin"),
        MexcAdapter("mexc"),
        HtxAdapter("htx"),
    ]


async def fetch_prices(client: HttpClient) -> List[PriceQuote]:
    adapters = build_cex_adapters() + build_dex_adapters()
    tasks = [adapter.fetch(client) for adapter in adapters]
    quotes: List[PriceQuote] = []
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for adapter, result in zip(adapters, results):
        if isinstance(result, Exception):
            meta = CEX_EXCHANGES.get(adapter.exchange_id) or DEX_EXCHANGES.get(adapter.exchange_id)
            if meta:
                quote = PriceQuote(
                    adapter.exchange_id,
                    meta.name,
                    meta.kind,
                    meta.chain,
                    0.0,
                    meta.source,
                    None,
                    datetime.now(timezone.utc),
                    meta.fee_bps,
                    [f"Fetch error: {result}"],
                )
                quotes.append(quote)
            continue
        quotes.append(result)
    return apply_staleness(quotes)


async def fetch_p2p(client: HttpClient) -> List[P2POffer]:
    adapters = build_p2p_adapters()
    tasks = [adapter.fetch_best_offer(client) for adapter in adapters]
    offers: List[P2POffer] = []
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception) or result is None:
            continue
        offers.append(result)
    return offers


async def run_once(client: HttpClient, order_size: float) -> None:
    quotes = await fetch_prices(client)
    p2p_offers = await fetch_p2p(client)
    rpc_slot = None
    try:
        rpc_slot = await SolanaRpc().get_slot(client)
    except Exception:
        rpc_slot = None
    ranking = build_ranking_result(quotes, p2p_offers, order_size)
    ranking.quotes.sort(key=lambda quote: quote.price_usd)
    top5_ids = [quote.exchange_id for quote in ranking.top5]
    render_summary(ranking, rpc_slot)
    render_quotes(ranking.quotes, top5_ids)
    render_top5(ranking.top5)
    render_p2p(ranking.best_p2p, p2p_offers)


async def main() -> None:
    parser = argparse.ArgumentParser(description="SOL price aggregator for CEX, DEX, and P2P sources.")
    parser.add_argument("--refresh", type=int, default=DEFAULT_REFRESH_SECONDS, help="Refresh interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run a single refresh cycle")
    parser.add_argument("--order-size", type=float, default=DEFAULT_ORDER_SIZE_USD, help="Order size for slippage checks")
    args = parser.parse_args()

    client = HttpClient()
    try:
        while True:
            await run_once(client, args.order_size)
            if args.once:
                break
            await asyncio.sleep(args.refresh)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
