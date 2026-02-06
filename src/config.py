from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExchangeMeta:
    name: str
    kind: str
    chain: str
    source: str
    fee_bps: float


CEX_EXCHANGES: Dict[str, ExchangeMeta] = {
    "binance": ExchangeMeta("Binance", "CEX", "Solana", "REST", 10),
    "gate": ExchangeMeta("Gate", "CEX", "Solana", "REST", 20),
    "bybit": ExchangeMeta("Bybit", "CEX", "Solana", "REST", 10),
    "okx": ExchangeMeta("OKX", "CEX", "Solana", "REST", 8),
    "bitget": ExchangeMeta("Bitget", "CEX", "Solana", "REST", 10),
    "coinbase": ExchangeMeta("Coinbase Exchange", "CEX", "Solana", "REST", 50),
    "upbit": ExchangeMeta("Upbit", "CEX", "Solana", "REST", 5),
    "kucoin": ExchangeMeta("KuCoin", "CEX", "Solana", "REST", 10),
    "mexc": ExchangeMeta("MEXC", "CEX", "Solana", "REST", 10),
    "htx": ExchangeMeta("HTX", "CEX", "Solana", "REST", 20),
}

DEX_EXCHANGES: Dict[str, ExchangeMeta] = {
    "raydium": ExchangeMeta("Raydium", "DEX", "Solana", "DexScreener", 30),
    "orca": ExchangeMeta("Orca", "DEX", "Solana", "DexScreener", 30),
    "jupiter": ExchangeMeta("Jupiter Aggregator", "DEX", "Solana", "Jupiter", 30),
    "meteora": ExchangeMeta("Meteora", "DEX", "Solana", "DexScreener", 30),
    "openbook": ExchangeMeta("OpenBook", "DEX", "Solana", "DexScreener", 20),
    "lifinity": ExchangeMeta("Lifinity", "DEX", "Solana", "DexScreener", 30),
    "saber": ExchangeMeta("Saber", "DEX", "Solana", "DexScreener", 20),
    "aldrin": ExchangeMeta("Aldrin", "DEX", "Solana", "DexScreener", 20),
    "saros": ExchangeMeta("Saros", "DEX", "Solana", "DexScreener", 20),
    "pumpfun": ExchangeMeta("Pump.fun / PumpSwap", "DEX", "Solana", "DexScreener", 50),
}

P2P_EXCHANGES: Dict[str, ExchangeMeta] = {
    "binance": ExchangeMeta("Binance P2P", "P2P", "Solana", "REST", 0),
    "bybit": ExchangeMeta("Bybit P2P", "P2P", "Solana", "REST", 0),
    "okx": ExchangeMeta("OKX P2P", "P2P", "Solana", "REST", 0),
    "gate": ExchangeMeta("Gate P2P", "P2P", "Solana", "REST", 0),
    "bitget": ExchangeMeta("Bitget P2P", "P2P", "Solana", "REST", 0),
}

REFERENCE_EXCHANGES = ["binance", "coinbase"]

DEFAULT_REFRESH_SECONDS = 15
DEFAULT_ORDER_SIZE_USD = 1000
