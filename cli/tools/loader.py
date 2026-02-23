from __future__ import annotations

"""Helpers for loading the truth CSV and transforming rows into domain records."""

from datetime import date, datetime
from pathlib import Path
from typing import List

import pandas as pd

from .domain import CaseRecord


def load_case_records(source: Path) -> List[CaseRecord]:
    """Read the CSV and return a list of cleaned CaseRecord items."""
    df = pd.read_csv(source, dtype={"CASE_NUMBER": "Int64"})
    cleaned = _prepare_dataframe(df)
    return _records_from_dataframe(cleaned)


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names, enforce required fields, and parse timestamps."""
    df.columns = df.columns.str.lower()
    required = {"case_number", "status", "application_submitted_date", "completed_date", "property_category"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["status"] = df["status"].fillna("").astype(str).str.strip().str.upper()
    df["property_category"] = df["property_category"].fillna("").astype(str).str.strip().str.upper()
    df["submitted_date"] = pd.to_datetime(df["application_submitted_date"], errors="coerce").dt.date
    df["completed_date"] = pd.to_datetime(df["completed_date"], errors="coerce").dt.date
    df["case_number"] = pd.to_numeric(df["case_number"], errors="coerce")
    return df


def _records_from_dataframe(df: pd.DataFrame) -> List[CaseRecord]:
    """Convert the prepared DataFrame rows into CaseRecord domain objects."""
    records: List[CaseRecord] = []
    for row in df.itertuples(index=False):
        if pd.isna(row.case_number):
            continue
        records.append(
            CaseRecord(
                case_number=int(row.case_number),
                status=row.status,
                property_category=row.property_category,
                submitted_date=_coerce_to_date(row.submitted_date),
                completed_date=_coerce_to_date(row.completed_date),
            )
        )
    return records


def _coerce_to_date(value: object | None) -> date | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return None
