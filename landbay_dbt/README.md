Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## Case Completion CLI

1. Install the dependencies listed in `requirements.txt`. If `uv sync` is unavailable, run this through the managed environment instead:
   ```
   uv run pip install -r requirements.txt
   ```
   This installs `pandas`, `matplotlib`, `python-dateutil`, and the UV tooling into `.venv/`.
2. Activate or run commands through the UV-managed environment before executing the CLI:
   - `uv activate` (Windows) or `uv shell` drops you into an interactive shell inside `.venv`.
   - For ad-hoc runs you can prefix the command with `uv run`, e.g.:
     ```
     uv run python -m landbay_dbt.cli 2021-02 --category STANDARD
     ```
   - Omitting `--category` evaluates all property types in the dataset.
3. The CLI reads `seeds/cases.csv`, mirrors the cleaning logic from `models/staging/stg_cases.sql`, filters by submission month (and optional property category), and buckets completed cases by the whole calendar-month difference between `APPLICATION_SUBMITTED_DATE` and `COMPLETED_DATE`.
4. A PNG plot lands under `plots/` (or another directory when passing `--output`). The file is named `case_completion_<YYYY_MM>_<category>.png` by default, and the terminal prints a short summary of counts and filters.

Documented assumptions:
- The seed `cases.csv` is the canonical source for this CLI because the repo does not ship a compiled dbt model or warehouse connection.
- The month difference is calculated via calendar-month arithmetic, and only records where `STATUS = 'COMPLETED'` with valid timestamps contribute to the buckets.