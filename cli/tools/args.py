from __future__ import annotations

"""Argument parsing helpers for the case completion CLI."""

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class CliArgs:
    month: date
    category: str | None
    source: Path
    output: Path | None


def _parse_month(value: str) -> date:
    try:
        parsed = datetime.strptime(value, "%Y-%m")
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Month must be YYYY-MM") from exc
    return date(parsed.year, parsed.month, 1)


def _normalize_category(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = value.strip().upper()
    return cleaned or None


def parse_args(argv: Sequence[str] | None, default_source: Path) -> CliArgs:
    """Parse CLI arguments and return a typed configuration object."""
    parser = argparse.ArgumentParser(
        description="Plot the distribution of case completion times for a submission month."
    )
    parser.add_argument("month", type=_parse_month, help="Month must be YYYY-MM.")
    parser.add_argument(
        "-c", "--category", type=str, default=None, help="Optional property category filter."
    )
    parser.add_argument(
        "-s", "--source", type=Path, default=default_source, help="Path to the cases CSV file."
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Optional explicit output path for the PNG plot."
    )
    args = parser.parse_args(argv)
    return CliArgs(
        month=args.month,
        category=_normalize_category(args.category),
        source=args.source,
        output=args.output,
    )
