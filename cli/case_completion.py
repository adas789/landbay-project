from __future__ import annotations

"""Entry point wiring for the case completion CLI."""

from pathlib import Path
from typing import Sequence

from .tools.args import parse_args
from .tools.bucketing import bucket_completion_months
from .tools.filtering import filter_records
from .tools.loader import load_case_records
from .tools.plotting import render_plot


CLI_ROOT = Path(__file__).resolve().parent


def _find_dbt_project_root() -> Path:
    for parent in (CLI_ROOT, *CLI_ROOT.parents):
        project_file = parent / "dbt_project.yml"
        if project_file.is_file():
            return parent
        nested_project = parent / "landbay_dbt" / "dbt_project.yml"
        if nested_project.is_file():
            return nested_project.parent
    raise FileNotFoundError("Could not locate dbt_project.yml near the CLI package location.")


DBT_PROJECT_ROOT = _find_dbt_project_root()
DEFAULT_SEED_PATH = DBT_PROJECT_ROOT / "seeds" / "cases.csv"
DEFAULT_PLOT_DIR = CLI_ROOT / "plots"


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
