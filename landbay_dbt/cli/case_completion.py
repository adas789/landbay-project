from __future__ import annotations

"""Entry point that orchestrates the case completion CLI workflow.

This module wires up argument parsing, data loading, filtering, bucketing, and
plotting so the responsibilities described in the tools directory stay isolated.
"""

from pathlib import Path
from typing import Sequence

from .tools.args import parse_args
from .tools.bucketing import bucket_completion_months
from .tools.filtering import filter_records
from .tools.loader import load_case_records
from .tools.plotting import render_plot

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED_PATH = PACKAGE_ROOT / "seeds" / "cases.csv"
DEFAULT_PLOT_DIR = PACKAGE_ROOT / "plots"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv, DEFAULT_SEED_PATH)
    records = load_case_records(args.source)
    filtered = filter_records(records, args.month, args.category)
    completed = sum(1 for record in filtered if record.is_completed())
    print(f"Loaded {len(records)} cases, {len(filtered)} submitted in {args.month:%Y-%m}.")
    context = f"Filtering by {args.category}" if args.category else "Including all property categories."
    print(context)
    print(f"Found {completed} completed cases out of {len(filtered)} submissions for the requested period.")
    bucket_counts = bucket_completion_months(filtered)
    output_path = render_plot(bucket_counts, args.month, args.category, DEFAULT_PLOT_DIR, override_path=args.output)
    print(f"Plot stored at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())