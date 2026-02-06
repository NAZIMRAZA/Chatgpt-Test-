from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class PriceQuote:
    exchange_id: str
    exchange_name: str
    kind: str
    chain: str
    price_usd: float
    source: str
    liquidity_usd: Optional[float]
    last_updated: datetime
    fee_bps: float
    warnings: List[str] = field(default_factory=list)


@dataclass
class P2POffer:
    exchange_id: str
    exchange_name: str
    price_usd: float
    payment_methods: List[str]
    min_limit: Optional[float]
    max_limit: Optional[float]
    merchant_count: Optional[int]
    region: Optional[str]
    last_updated: datetime


@dataclass
class RankingResult:
    quotes: List[PriceQuote]
    top5: List[PriceQuote]
    average_price: Optional[float]
    reference_price: Optional[float]
    best_p2p: Optional[P2POffer]
    slippage_warning: Optional[str]
