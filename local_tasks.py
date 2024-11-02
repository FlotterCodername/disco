"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent


def main() -> int:
    """
    The main function point for the pre-commit hook

    :return: exit code
    """
    # List of files passed to the hook
    _: list[Path] = [REPO_ROOT / i for i in sys.argv[1:]]
    return 0


if __name__ == "__main__":
    sys.exit(main())
