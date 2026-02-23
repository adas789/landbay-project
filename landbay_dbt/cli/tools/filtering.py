from __future__ import annotations

"""Filtering helpers to reduce the dataset to the requested submission window.

The filtering logic assumes the loader already produced clean timestamps; here
we simply slice on submission month and optional property category.
"""

from datetime import date
from typing import Iterable, List

from .domain import CaseRecord


def filter_records(records: Iterable[CaseRecord], month: date, category: str | None) -> List[CaseRecord]:
    """Return only the rows submitted in the requested window/category."""
    return [record for record in records if _submitted_in_month(record, month) and _matches_category(record, category)]


def _submitted_in_month(record: CaseRecord, month: date) -> bool:
    submitted = record.submitted_date
    return submitted is not None and submitted.year == month.year and submitted.month == month.month


def _matches_category(record: CaseRecord, category: str | None) -> bool:
    return category is None or record.property_category == category