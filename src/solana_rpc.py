from __future__ import annotations

import os
from typing import Any, Dict

from src.http import HttpClient


class SolanaRpc:
    def __init__(self, endpoint: str | None = None) -> None:
        self.endpoint = endpoint or os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

    async def _rpc(self, client: HttpClient, method: str, params: list | None = None) -> Dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or [],
        }
        return await client.post_json(self.endpoint, payload, ttl=5)

    async def get_slot(self, client: HttpClient) -> int:
        data = await self._rpc(client, "getSlot")
        return int(data.get("result", 0))
