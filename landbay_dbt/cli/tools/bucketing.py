from __future__ import annotations

"""Bucket completed cases by the number of calendar months it took to finish.

Only records reporting a non-negative month delta are counted; the caller can
inspect the dict for zero-frequency months if necessary.
"""

from collections import Counter
from typing import Iterable

from .domain import CaseRecord


def bucket_completion_months(records: Iterable[CaseRecord]) -> dict[int, int]:
    """Return a sorted mapping from months-to-complete → case count."""
    counter: Counter[int] = Counter()
    for record in records:
        months = record.months_to_complete()
        if months is None:
            continue
        counter[months] += 1
    return dict(sorted(counter.items()))