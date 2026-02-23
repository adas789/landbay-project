from __future__ import annotations

"""Matplotlib helpers for rendering the completion histogram."""

from datetime import date
from pathlib import Path
from typing import Mapping

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render_plot(
    buckets: Mapping[int, int],
    month: date,
    category: str | None,
    output_dir: Path,
    override_path: Path | None = None,
) -> Path:
    """Create the plot and return the location of the saved PNG."""
    output_dir.mkdir(parents=True, exist_ok=True)
    labels = sorted(buckets.keys())
    values = [buckets[label] for label in labels]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if labels:
        ax.bar(labels, values, color="#1f77b4")
        ax.set_xticks(labels)
    else:
        ax.text(0.5, 0.5, "No completed cases to plot", ha="center", va="center", transform=ax.transAxes)
    ax.set_xlabel("Months between submission and completion")
    ax.set_ylabel("Number of cases")
    context = category or "All categories"
    ax.set_title(f"Case completions for {month:%Y-%m} — {context}")
    fig.tight_layout()
    output_path = override_path or _default_output_path(output_dir, month, category)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def _default_output_path(output_dir: Path, month: date, category: str | None) -> Path:
    safe_category = (category or "all").replace(" ", "_").lower()
    filename = f"case_completion_{month:%Y_%m}_{safe_category}.png"
    return output_dir / filename
