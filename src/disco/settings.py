"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from disco.paths import DISCO_DB

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DISCO_DB}}
INSTALLED_APPS = ["disco"]
USE_TZ = True
