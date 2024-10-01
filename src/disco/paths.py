"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
from pathlib import Path

from disco import __repo_root__
from disco.definitions import EV

DISCO_HOME = Path(os.getenv(EV.DISCO_HOME, Path.home() / ".disco")).resolve()
if os.getenv(EV.DISCO_IS_DOCKER):
    DISCO_HOME = Path("/var/disco")

DISCO_RUN = DISCO_HOME / "run"
DISCO_RUN.mkdir(parents=True, exist_ok=True)
PODCASTS_TOML = DISCO_RUN / "podcasts.toml"
SECRETS_TOML = DISCO_RUN / "secrets.toml"

DISCO_LOG = DISCO_HOME / "log"
DISCO_LOG.mkdir(parents=True, exist_ok=True)

DISCO_SQLITE = DISCO_HOME / "sqlite"
DISCO_SQLITE.mkdir(parents=True, exist_ok=True)
DISCO_DB = DISCO_SQLITE / "db.sqlite3"

# DJANGO
MANAGE_PY = __repo_root__ / "manage.py"
