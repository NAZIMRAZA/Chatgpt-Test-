from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from src.adapters.base import PriceAdapter
from src.config import DEX_EXCHANGES
from src.http import HttpClient
from src.models import PriceQuote


DEXSCREENER_SEARCH_URL = "https://api.dexscreener.com/latest/dex/search"


class DexScreenerAdapter(PriceAdapter):
    dex_id: str

    def __init__(self, exchange_id: str, dex_id: str) -> None:
        super().__init__(exchange_id)
        self.dex_id = dex_id

    async def fetch(self, client: HttpClient) -> PriceQuote:
        params = {"q": "SOL/USDC"}
        data = await client.get_json(DEXSCREENER_SEARCH_URL, params=params, ttl=10)
        pairs = [
            pair
            for pair in data.get("pairs", [])
            if pair.get("chainId") == "solana" and pair.get("dexId") == self.dex_id
        ]
        if not pairs:
            raise RuntimeError(f"No DexScreener pairs found for {self.dex_id}")
        best_pair = max(pairs, key=lambda item: float(item.get("liquidity", {}).get("usd", 0)))
        price = float(best_pair["priceUsd"])
        liquidity = float(best_pair.get("liquidity", {}).get("usd", 0))
        meta = DEX_EXCHANGES[self.exchange_id]
        warnings = []
        if liquidity < 100000:
            warnings.append("Low liquidity")
        return PriceQuote(
            self.exchange_id,
            meta.name,
            meta.kind,
            meta.chain,
            price,
            meta.source,
            liquidity,
            datetime.now(timezone.utc),
            meta.fee_bps,
            warnings,
        )


class JupiterAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://price.jup.ag/v6/price", params={"ids": "SOL"}, ttl=5)
        price = float(data["data"]["SOL"]["price"])
        meta = DEX_EXCHANGES[self.exchange_id]
        return PriceQuote(
            self.exchange_id,
            meta.name,
            meta.kind,
            meta.chain,
            price,
            meta.source,
            None,
            datetime.now(timezone.utc),
            meta.fee_bps,
            ["Aggregator pricing"],
        )


def build_dex_adapters() -> list[PriceAdapter]:
    return [
        DexScreenerAdapter("raydium", "raydium"),
        DexScreenerAdapter("orca", "orca"),
        JupiterAdapter("jupiter"),
        DexScreenerAdapter("meteora", "meteora"),
        DexScreenerAdapter("openbook", "openbook"),
        DexScreenerAdapter("lifinity", "lifinity"),
        DexScreenerAdapter("saber", "saber"),
        DexScreenerAdapter("aldrin", "aldrin"),
        DexScreenerAdapter("saros", "saros"),
        DexScreenerAdapter("pumpfun", "pumpfun"),
    ]
