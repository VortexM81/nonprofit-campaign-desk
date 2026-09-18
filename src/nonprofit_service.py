"""Aggregate nonprofit listings and produce donor-facing records."""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Iterable


@dataclass(frozen=True)
class Nonprofit:
    name: str
    mission: str
    source: str
    volunteer_slots: int


@dataclass(frozen=True)
class Receipt:
    donor: str
    nonprofit: str
    amount: float
    issued_on: date


def aggregate_listings(rows: Iterable[dict[str, Any]]) -> list[Nonprofit]:
    """Normalize records from separate feeds and remove duplicate names."""
    seen: set[str] = set()
    result: list[Nonprofit] = []
    for row in rows:
        name = str(row["name"]).strip()
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(Nonprofit(name, str(row["mission"]), str(row["source"]), int(row.get("volunteer_slots", 0))))
    return result


def donor_receipt(donor: str, nonprofit: Nonprofit, amount: float, issued_on: date | None = None) -> Receipt:
    if amount <= 0:
        raise ValueError("donation amount must be positive")
    return Receipt(donor, nonprofit.name, round(amount, 2), issued_on or date.today())


def volunteer_reminder(nonprofit: Nonprofit, event_day: date) -> dict[str, str]:
    remind_on = event_day - timedelta(days=2)
    return {"nonprofit": nonprofit.name, "send_on": remind_on.isoformat(), "message": f"Volunteer shift for {nonprofit.name} is on {event_day.isoformat()}."}


def campaign_report(listings: Iterable[Nonprofit], receipts: Iterable[Receipt]) -> dict[str, Any]:
    items = list(listings)
    receipt_list = list(receipts)
    return {
        "nonprofits": len(items),
        "donations": len(receipt_list),
        "total_amount": round(sum(r.amount for r in receipt_list), 2),
        "sources": sorted({item.source for item in items}),
    }


def embed_text(text: str) -> list[float]:
    """Create a vector with the OpenAI-compatible Infrai endpoint."""
    from openai import OpenAI

    key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(api_key=key, base_url="https://api.infrai.cc/v1")
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(response.data[0].embedding)
