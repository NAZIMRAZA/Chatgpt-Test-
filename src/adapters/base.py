from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.http import HttpClient
from src.models import P2POffer, PriceQuote


class PriceAdapter(ABC):
    def __init__(self, exchange_id: str) -> None:
        self.exchange_id = exchange_id

    @abstractmethod
    async def fetch(self, client: HttpClient) -> PriceQuote:
        raise NotImplementedError


class P2PAdapter(ABC):
    def __init__(self, exchange_id: str) -> None:
        self.exchange_id = exchange_id

    @abstractmethod
    async def fetch_best_offer(self, client: HttpClient) -> Optional[P2POffer]:
        raise NotImplementedError
