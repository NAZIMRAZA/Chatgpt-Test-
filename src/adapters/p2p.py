from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from src.adapters.base import P2PAdapter
from src.config import P2P_EXCHANGES
from src.http import HttpClient
from src.models import P2POffer


class BinanceP2PAdapter(P2PAdapter):
    async def fetch_best_offer(self, client: HttpClient) -> Optional[P2POffer]:
        payload = {
            "asset": "SOL",
            "fiat": "USD",
            "tradeType": "BUY",
            "page": 1,
            "rows": 10,
            "payTypes": [],
            "publisherType": None,
        }
        data = await client.post_json("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", payload, ttl=10)
        offers = data.get("data", [])
        if not offers:
            return None
        best = offers[0]
        meta = P2P_EXCHANGES[self.exchange_id]
        return P2POffer(
            self.exchange_id,
            meta.name,
            float(best["adv"]["price"]),
            [payment["identifier"] for payment in best["adv"].get("tradeMethods", [])],
            float(best["adv"].get("minSingleTransAmount", 0)),
            float(best["adv"].get("maxSingleTransAmount", 0)),
            None,
            best["adv"].get("country"),
            datetime.now(timezone.utc),
        )


class BybitP2PAdapter(P2PAdapter):
    async def fetch_best_offer(self, client: HttpClient) -> Optional[P2POffer]:
        params = {
            "tokenId": "SOL",
            "currencyId": "USD",
            "side": 1,
            "page": 1,
            "size": 10,
        }
        data = await client.get_json("https://api2.bybit.com/fiat/otc/item/online", params=params, ttl=10)
        items = data.get("result", {}).get("items", [])
        if not items:
            return None
        best = items[0]
        meta = P2P_EXCHANGES[self.exchange_id]
        return P2POffer(
            self.exchange_id,
            meta.name,
            float(best["price"]),
            [method.get("paymentName") for method in best.get("payments", [])],
            float(best.get("minAmount", 0)),
            float(best.get("maxAmount", 0)),
            None,
            None,
            datetime.now(timezone.utc),
        )


class OkxP2PAdapter(P2PAdapter):
    async def fetch_best_offer(self, client: HttpClient) -> Optional[P2POffer]:
        params = {
            "baseCurrency": "SOL",
            "quoteCurrency": "USD",
            "side": "buy",
            "paymentMethod": "all",
            "userType": "all",
            "showTrade": "false",
            "showFollow": "false",
            "showAlreadyTraded": "false",
            "isAbleFilter": "false",
        }
        data = await client.get_json("https://www.okx.com/v3/c2c/tradingOrders/books", params=params, ttl=10)
        offers = data.get("data", {}).get("sell", [])
        if not offers:
            return None
        best = offers[0]
        meta = P2P_EXCHANGES[self.exchange_id]
        return P2POffer(
            self.exchange_id,
            meta.name,
            float(best["price"]),
            [method.get("payMethod") for method in best.get("paymentMethods", [])],
            float(best.get("minAmount", 0)),
            float(best.get("maxAmount", 0)),
            None,
            best.get("quoteName"),
            datetime.now(timezone.utc),
        )


class GateP2PAdapter(P2PAdapter):
    async def fetch_best_offer(self, client: HttpClient) -> Optional[P2POffer]:
        params = {
            "currency": "SOL",
            "fiat": "USD",
            "side": "buy",
            "page": 1,
            "limit": 10,
        }
        data = await client.get_json("https://www.gate.io/json_svr/query/?u=1&c=otc&a=order_list", params=params, ttl=10)
        offers = data.get("data", []) if isinstance(data, dict) else []
        if not offers:
            return None
        best = offers[0]
        meta = P2P_EXCHANGES[self.exchange_id]
        return P2POffer(
            self.exchange_id,
            meta.name,
            float(best.get("price", 0)),
            [method for method in best.get("payTypes", [])],
            float(best.get("min", 0)),
            float(best.get("max", 0)),
            None,
            None,
            datetime.now(timezone.utc),
        )


class BitgetP2PAdapter(P2PAdapter):
    async def fetch_best_offer(self, client: HttpClient) -> Optional[P2POffer]:
        params = {
            "side": "buy",
            "coin": "SOL",
            "fiat": "USD",
            "pageSize": 10,
            "pageNo": 1,
        }
        data = await client.get_json("https://api.bitget.com/api/v2/express/otc/advertList", params=params, ttl=10)
        offers = data.get("data", [])
        if not offers:
            return None
        best = offers[0]
        meta = P2P_EXCHANGES[self.exchange_id]
        return P2POffer(
            self.exchange_id,
            meta.name,
            float(best.get("price", 0)),
            best.get("payMethods", []),
            float(best.get("minTradeAmount", 0)),
            float(best.get("maxTradeAmount", 0)),
            None,
            None,
            datetime.now(timezone.utc),
        )


def build_p2p_adapters() -> list[P2PAdapter]:
    return [
        BinanceP2PAdapter("binance"),
        BybitP2PAdapter("bybit"),
        OkxP2PAdapter("okx"),
        GateP2PAdapter("gate"),
        BitgetP2PAdapter("bitget"),
    ]
