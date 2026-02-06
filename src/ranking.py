from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import List, Optional, Tuple

from src.config import DEFAULT_ORDER_SIZE_USD, REFERENCE_EXCHANGES
from src.models import P2POffer, PriceQuote, RankingResult


def compute_reference_price(quotes: List[PriceQuote]) -> Optional[float]:
    ref_prices = [quote.price_usd for quote in quotes if quote.exchange_id in REFERENCE_EXCHANGES]
    if not ref_prices:
        return None
    return mean(ref_prices)


def compute_average_price(quotes: List[PriceQuote]) -> Optional[float]:
    if not quotes:
        return None
    return mean(quote.price_usd for quote in quotes)


def apply_liquidity_checks(quotes: List[PriceQuote], order_size: float) -> List[PriceQuote]:
    for quote in quotes:
        if quote.kind != "DEX":
            continue
        if quote.liquidity_usd is None:
            quote.warnings.append("No liquidity data")
            continue
        price_impact = min(order_size / max(quote.liquidity_usd, 1), 0.05)
        if price_impact > 0.01:
            quote.warnings.append(f"Price impact {price_impact:.2%}")
    return quotes


def apply_spread_checks(quotes: List[PriceQuote], reference: Optional[float]) -> List[PriceQuote]:
    if reference is None:
        return quotes
    for quote in quotes:
        spread = abs(quote.price_usd - reference) / reference
        if spread > 0.02:
            quote.warnings.append(f"Abnormal spread {spread:.2%}")
    return quotes


def rank_quotes(quotes: List[PriceQuote], order_size: float, reference: Optional[float]) -> List[Tuple[PriceQuote, float]]:
    ranked: List[Tuple[PriceQuote, float]] = []
    for quote in quotes:
        fee_multiplier = 1 + (quote.fee_bps / 10000)
        slippage_cost = 0.0
        if quote.kind == "DEX" and quote.liquidity_usd:
            slippage_cost = min(order_size / max(quote.liquidity_usd, 1), 0.05) * quote.price_usd
        effective_price = quote.price_usd * fee_multiplier + slippage_cost
        ranked.append((quote, effective_price))
    ranked.sort(key=lambda item: item[1])
    return ranked


def build_ranking_result(
    quotes: List[PriceQuote],
    p2p_offers: List[P2POffer],
    order_size: float = DEFAULT_ORDER_SIZE_USD,
) -> RankingResult:
    valid_quotes = [quote for quote in quotes if quote.price_usd > 0]
    reference_price = compute_reference_price(valid_quotes)
    average_price = compute_average_price(valid_quotes)
    valid_quotes = apply_liquidity_checks(valid_quotes, order_size)
    valid_quotes = apply_spread_checks(valid_quotes, reference_price)
    ranked = rank_quotes(valid_quotes, order_size, reference_price)
    top5 = [item[0] for item in ranked[:5]]

    best_p2p = min(p2p_offers, key=lambda offer: offer.price_usd) if p2p_offers else None

    slippage_warning = None
    for quote in valid_quotes:
        if any("Price impact" in warning for warning in quote.warnings):
            slippage_warning = "Some DEX pools show elevated price impact for the configured order size."
            break

    return RankingResult(
        quotes=quotes,
        top5=top5,
        average_price=average_price,
        reference_price=reference_price,
        best_p2p=best_p2p,
        slippage_warning=slippage_warning,
    )
