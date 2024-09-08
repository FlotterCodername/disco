"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
from pathlib import Path

from disco.definitions import EV

DISCO_RUN = Path(os.getenv(EV.DISCO_RUN, Path.home() / ".disco" / "run")).resolve()
DISCO_LOG = Path(os.getenv(EV.DISCO_LOG, Path.home() / ".disco" / "log")).resolve()
if os.getenv(EV.DISCO_IS_DOCKER):
    DISCO_RUN = Path("/var/disco/run/")
    DISCO_LOG = Path("/var/disco/log/")
SECRETS_JSON = DISCO_RUN / "secrets.json"
