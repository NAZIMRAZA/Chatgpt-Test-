from __future__ import annotations

from datetime import datetime, timezone

from src.adapters.base import PriceAdapter
from src.config import CEX_EXCHANGES
from src.http import HttpClient
from src.models import PriceQuote


class BinanceAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.binance.com/api/v3/ticker/price", params={"symbol": "SOLUSDT"})
        price = float(data["price"])
        meta = CEX_EXCHANGES[self.exchange_id]
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, None, datetime.now(timezone.utc), meta.fee_bps)


class GateAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.gateio.ws/api/v4/spot/tickers", params={"currency_pair": "SOL_USDT"})
        price = float(data[0]["last"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data[0].get("quote_volume", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)


class BybitAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json(
            "https://api.bybit.com/v5/market/tickers",
            params={"category": "spot", "symbol": "SOLUSDT"},
        )
        price = float(data["result"]["list"][0]["lastPrice"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data["result"]["list"][0].get("turnover24h", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)


class OkxAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://www.okx.com/api/v5/market/ticker", params={"instId": "SOL-USDT"})
        price = float(data["data"][0]["last"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data["data"][0].get("volCcy24h", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)


class BitgetAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.bitget.com/api/v2/spot/market/tickers", params={"symbol": "SOLUSDT"})
        price = float(data["data"][0]["lastPr"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data["data"][0].get("quoteVol", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)


class CoinbaseAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.exchange.coinbase.com/products/SOL-USD/ticker")
        price = float(data["price"])
        meta = CEX_EXCHANGES[self.exchange_id]
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, None, datetime.now(timezone.utc), meta.fee_bps)


class UpbitAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.upbit.com/v1/ticker", params={"markets": "USDT-SOL"})
        price = float(data[0]["trade_price"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data[0].get("acc_trade_price_24h", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)


class KuCoinAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.kucoin.com/api/v1/market/orderbook/level1", params={"symbol": "SOL-USDT"})
        price = float(data["data"]["price"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data["data"].get("volValue", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)


class MexcAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.mexc.com/api/v3/ticker/price", params={"symbol": "SOLUSDT"})
        price = float(data["price"])
        meta = CEX_EXCHANGES[self.exchange_id]
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, None, datetime.now(timezone.utc), meta.fee_bps)


class HtxAdapter(PriceAdapter):
    async def fetch(self, client: HttpClient) -> PriceQuote:
        data = await client.get_json("https://api.huobi.pro/market/trade", params={"symbol": "solusdt"})
        price = float(data["tick"]["data"][0]["price"])
        meta = CEX_EXCHANGES[self.exchange_id]
        liquidity = float(data["tick"].get("amount", 0))
        return PriceQuote(self.exchange_id, meta.name, meta.kind, meta.chain, price, meta.source, liquidity, datetime.now(timezone.utc), meta.fee_bps)
