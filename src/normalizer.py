from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List

from src.models import PriceQuote


STALE_AFTER_SECONDS = 30


def apply_staleness(quotes: List[PriceQuote]) -> List[PriceQuote]:
    now = datetime.now(timezone.utc)
    for quote in quotes:
        if now - quote.last_updated > timedelta(seconds=STALE_AFTER_SECONDS):
            quote.warnings.append("Stale data")
    return quotes
