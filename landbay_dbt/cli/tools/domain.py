from __future__ import annotations

"""Domain value objects used by the case completion CLI.

This module exposes the lightweight `CaseRecord` dataclass and encapsulates
any derived metrics so other layers can operate in terms of business concepts
without re-implementing the calendar-month logic.
"""

from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta


@dataclass(frozen=True)
class CaseRecord:
    case_number: int
    status: str
    property_category: str
    submitted_date: date | None
    completed_date: date | None

    def is_completed(self) -> bool:
        return self.status == "COMPLETED" and self.completed_date is not None

    def months_to_complete(self) -> int | None:
        if not self.is_completed() or self.submitted_date is None:
            return None
        delta = relativedelta(self.completed_date, self.submitted_date)
        total_months = delta.years * 12 + delta.months
        return total_months if total_months >= 0 else None