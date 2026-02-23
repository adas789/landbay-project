## Case Completion CLI

Minimal CLI that loads `landbay_dbt/seeds/cases.csv`, mirrors the cleaning/filtering in `landbay_dbt/models/staging/stg_cases.sql`, and plots the months-between-submission/completion distribution for a chosen submission month.

### Prerequisites
1. Clone the repo so that `cli/` and `landbay_dbt/` live next to one another in the workspace root (`landbay_dbt` must contain `dbt_project.yml`).
2. Ensure you have Python 3.13+ available. Install dependencies through `uv` once per checkout:
   ```
   uv run python -m pip install -r requirements.txt
   ```
   This command seeds the `.venv/` that `uv` manages. If you see `ModuleNotFoundError: pip`, run `uv run python -m ensurepip --upgrade` and retry the install.
3. Work from inside the `uv` environment: either run `uv activate` (Windows) / `uv shell` (Unix) or prefix every command with `uv run`. This keeps the requirements constrained to the `.venv` instead of the system Python.
4. Confirm the install with `uv run python -m pip list` (or `uv run python -m pip check` to detect conflicts) before running the CLI.

### Running the CLI
Execute the package from the workspace root so that the CLI can locate `landbay_dbt/seeds/cases.csv`:
```text
uv run python -m cli 2021-02 --category STANDARD
```
| Flag | Description |
| --- | --- |
| `month` (required) | Submission month in `YYYY-MM` format (e.g., `2021-02`). This filters `APPLICATION_SUBMITTED_DATE`. |
| `--category` / `-c` | Optional property category. Values are upper-cased (e.g., `STANDARD`, `REVIEW`). Omit to show all categories. |
| `--source` / `-s` | Point to an alternate cases CSV if you are working with a different dataset. Defaults to `landbay_dbt/seeds/cases.csv`. |
| `--output` / `-o` | Override the PNG path. When unset the plot goes to `cli/plots/case_completion_<month>_<category>.png`. |

After running you will see a summary of loaded rows and completed cases. The plot is written under `cli/plots/` unless you use `--output`. Open the PNG with your preferred image viewer.

#### Examples
- `uv run python -m cli 2021-03` (plots every category for March 2021).  
- `uv run python -m cli 2020-11 --category REVIEW --output reports/review_2020_11.png` (uses a different output path).

### Important files
- `requirements.txt` – update and reinstall with the `uv` command whenever you add dependencies.  
- `landbay_dbt/seeds/cases.csv` – primary dataset; must include `CASE_NUMBER`, `STATUS`, `APPLICATION_SUBMITTED_DATE`, `COMPLETED_DATE`, and `PROPERTY_CATEGORY`.  
- `landbay_dbt/models/staging/stg_cases.sql` – SQL reference for the Python filtering logic.

For dbt background (models, macros, etc.) refer to `landbay_dbt/README.md`.

### Troubleshooting
- If the `uv run` command errors with `cd landbay-project` not found, it usually means you already `cd`'d into `landbay-project` before running the command; just run `uv run ...` without the extra `cd`.  
- Missing columns raise `ValueError: Missing required columns: {...}`; double-check that `landbay_dbt/seeds/cases.csv` has the expected headers in lower-underscore form.  
- After editing `requirements.txt`, rerun `uv run python -m pip install -r requirements.txt` so the CLI still executes in the managed environment.
