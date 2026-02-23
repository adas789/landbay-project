from __future__ import annotations

"""Allow the standalone CLI package to be executed via ``python -m``."""

from .case_completion import main


if __name__ == "__main__":
    raise SystemExit(main())
