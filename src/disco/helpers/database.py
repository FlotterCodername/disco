"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import subprocess
import sys

from disco import __product__
from disco.models import Podcast
from disco.paths import MANAGE_PY


def bootstrap() -> None:
    """Bootstrap the database."""
    subprocess.run([sys.executable, MANAGE_PY, "makemigrations", __product__], check=True)
    subprocess.run([sys.executable, MANAGE_PY, "migrate", __product__], check=True)
    Podcast.load_from_configuration()
