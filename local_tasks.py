"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent


def main() -> int:
    """
    The main function point for the pre-commit hook

    :return: exit code
    """
    # List of files passed to the hook
    files: list[Path] = [REPO_ROOT / i for i in sys.argv[1:]]
    if any(i.suffix.casefold() == ".py" for i in files) or not files:
        return apidoc()
    return 0


def apidoc() -> int:
    """
    Run sphinx-apidoc

    :return: exit code
    """
    command: list[str | Path] = [
        "sphinx-apidoc",
        REPO_ROOT / "src",
        "--output-dir",
        REPO_ROOT / "docs" / "api",
        "-q",
        "--force",
        "--module-first",
        "--no-toc",
        "--remove-old",
    ]
    try:
        return subprocess.run(command, cwd=REPO_ROOT).returncode
    except FileNotFoundError:
        print("The command sphinx-apidoc is unavailable. Skipping this task silently.", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
