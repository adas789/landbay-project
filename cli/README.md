## Case Completion CLI

This package bundles a lightweight CLI that reads `seeds/cases.csv`, applies the same filtering and cleaning as `models/staging/stg_cases.sql`, and plots the distribution of months between submission and completion for a user-selected window.

### Prerequisites
1. Clone the repository so that `cli/` and `landbay_dbt/` sit side by side in the workspace root.
2. Install dependencies with the UV-managed tooling (the `requirements.txt` file already lists `pandas`, `matplotlib`, `python-dateutil`, and `uv`):
   ```
   uv run pip install -r requirements.txt
   ```
   Run this command only once after cloning; it populates the `.venv/` directory that `uv` uses under the hood.
3. Enter the virtual environment with `uv activate` (Windows) or `uv shell`, or prefix each invocation with `uv run` when you just need to execute a single command.

### Running the CLI
1. From the workspace root, use the relocated CLI package at the top level:
   ```
   uv run python -m cli 2021-02 --category STANDARD
   ```
2. Swap `2021-02` for the desired submission month and drop `--category` to process every property type. The tool filters on submission month, then counts completed cases by the calendar-month delta between `APPLICATION_SUBMITTED_DATE` and `COMPLETED_DATE`.
3. By default the PNG is saved under the CLI package's own `plots/` directory (e.g. `cli/plots/case_completion_2021_02_standard.png`). Supply `--output` to point to another directory/filename if you want to capture results elsewhere.

### Files to know
- `requirements.txt` – brand new dependencies for this CLI; update it if you add packages before re-running the installation command.
- `landbay_dbt/seeds/cases.csv` – the CSV file the CLI consumes as its primary dataset.
- `landbay_dbt/models/staging/stg_cases.sql` – reference for the cleaning logic the CLI mirrors.

For dbt-specific background (model hierarchy, sources, macros), see `landbay_dbt/README.md`.
