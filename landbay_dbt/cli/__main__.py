from __future__ import annotations

"""Package entrypoint allowing the CLI to be executed via ``python -m``."""

from .case_completion import main


if __name__ == "__main__":
    raise SystemExit(main())