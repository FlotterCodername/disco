"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
from pathlib import Path

from disco.definitions import EV

DISCO_HOME = Path(os.getenv(EV.DISCO_HOME, Path.home() / ".disco")).resolve()
if os.getenv(EV.DISCO_IS_DOCKER):
    DISCO_HOME = Path("/var/disco")

DISCO_RUN = DISCO_HOME / "run"
SECRETS_JSON = DISCO_RUN / "secrets.json"

DISCO_LOG = DISCO_HOME / "log"

DISCO_SQLITE = DISCO_HOME / "sqlite"
