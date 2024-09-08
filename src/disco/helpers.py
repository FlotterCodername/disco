"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import json
import sys

import keyring
from atomicwrites import atomic_write

from disco.definitions import SERVICE_NAME, USERNAME
from disco.paths import SECRETS_JSON


def get_discord_bot_token() -> str:
    """
    Get the Discord bot token from the secrets file or keyring,
    and scrub it from the secrets file atomically using atomicwrites.

    :return: The Discord bot token
    """
    try:
        if SECRETS_JSON.is_file():
            loaded = json.loads(SECRETS_JSON.read_text())
            token = loaded[SERVICE_NAME][USERNAME]
            loaded[SERVICE_NAME][USERNAME] = None
            with atomic_write(SECRETS_JSON, mode="w", overwrite=True) as f:
                json.dump(loaded, f)
            return token
        # to store token: keyring.set_password(SERVICE_NAME, USERNAME, "<your token>")
        return keyring.get_password(SERVICE_NAME, USERNAME)
    except Exception:
        print("Failed to obtain token.")
        sys.exit(1)
