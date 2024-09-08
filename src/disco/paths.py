"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
from pathlib import Path

DISCO_RUN = Path(os.getenv("DISCO_RUN", Path.home() / ".disco")).resolve()
if os.getenv("DISCO_IS_DOCKER"):
    DISCO_RUN = Path("/run/disco/")
SECRETS_JSON = DISCO_RUN / "secrets.json"
