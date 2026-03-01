"""Entry point: python -m cli"""

import asyncio
import sys

from .app import run


def main() -> None:
    # Use UTF-8 for Unicode box-drawing on Windows
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    asyncio.run(run())


if __name__ == "__main__":
    main()
