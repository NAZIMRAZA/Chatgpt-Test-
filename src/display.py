from __future__ import annotations

from datetime import datetime
from typing import List

from rich.console import Console
from rich.table import Table

from src.models import P2POffer, PriceQuote, RankingResult


console = Console()


def format_time(ts: datetime) -> str:
    return ts.strftime("%H:%M:%S UTC")


def render_quotes(quotes: List[PriceQuote], top5_ids: List[str]) -> None:
    table = Table(title="SOL Price Snapshot")
    table.add_column("Rank", justify="right")
    table.add_column("Exchange")
    table.add_column("Type")
    table.add_column("Chain")
    table.add_column("SOL Price (USD)", justify="right")
    table.add_column("Source")
    table.add_column("Liquidity", justify="right")
    table.add_column("Last Updated")

    for idx, quote in enumerate(quotes, start=1):
        highlight = "*" if quote.exchange_id in top5_ids else ""
        liquidity = f"${quote.liquidity_usd:,.0f}" if quote.liquidity_usd else "N/A"
        table.add_row(
            f"{idx}{highlight}",
            quote.exchange_name,
            quote.kind,
            quote.chain,
            f"${quote.price_usd:,.4f}",
            quote.source,
            liquidity,
            format_time(quote.last_updated),
        )
    console.print(table)


def render_top5(top5: List[PriceQuote]) -> None:
    table = Table(title="Top 5 Cheapest SOL Sources")
    table.add_column("Rank", justify="right")
    table.add_column("Exchange")
    table.add_column("Type")
    table.add_column("Price (USD)", justify="right")
    table.add_column("Warnings")
    for idx, quote in enumerate(top5, start=1):
        warnings = "; ".join(quote.warnings) if quote.warnings else ""
        table.add_row(str(idx), quote.exchange_name, quote.kind, f"${quote.price_usd:,.4f}", warnings)
    console.print(table)


def render_p2p(best: P2POffer | None, offers: List[P2POffer]) -> None:
    if not best:
        console.print("[yellow]No P2P offers available.[/yellow]")
        return
    console.print(
        f"[bold green]Best P2P Buy Rate:[/bold green] {best.exchange_name} at ${best.price_usd:,.4f}"
    )
    table = Table(title="P2P Cheapest Offers")
    table.add_column("Exchange")
    table.add_column("Price")
    table.add_column("Payment Methods")
    table.add_column("Min")
    table.add_column("Max")
    table.add_column("Region")
    for offer in offers:
        table.add_row(
            offer.exchange_name,
            f"${offer.price_usd:,.4f}",
            ", ".join(offer.payment_methods) if offer.payment_methods else "N/A",
            f"${offer.min_limit:,.2f}" if offer.min_limit else "N/A",
            f"${offer.max_limit:,.2f}" if offer.max_limit else "N/A",
            offer.region or "N/A",
        )
    console.print(table)


def render_summary(result: RankingResult, rpc_slot: int | None = None) -> None:
    if result.reference_price:
        console.print(f"USD Reference Price (Binance + Coinbase): ${result.reference_price:,.4f}")
    if result.average_price:
        console.print(f"Global Average SOL Price: ${result.average_price:,.4f}")
    if rpc_slot:
        console.print(f"Solana RPC Slot: {rpc_slot}")
    if result.slippage_warning:
        console.print(f"[yellow]{result.slippage_warning}[/yellow]")
