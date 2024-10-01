"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import json
import logging
from logging import handlers

import keyring

from disco import __product__
from disco.definitions import SERVICE_NAME, USERNAME
from disco.helpers.atomicwrites import atomic_write
from disco.paths import DISCO_LOG, SECRETS_JSON


def get_log_handler() -> handlers.RotatingFileHandler:
    """
    Configure the logging for the bot (taken from `discord.py docs
    <https://discordpy.readthedocs.io/en/v2.4.0/logging.html>`_.)

    :return: The logging handler
    """
    DISCO_LOG.mkdir(parents=True, exist_ok=True)
    handler = handlers.RotatingFileHandler(
        filename=DISCO_LOG / f"{__product__}.log", encoding="utf-8", maxBytes=32 * 1024 * 1024, backupCount=5
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    handler.setFormatter(formatter)
    return handler


def get_discord_bot_token(scrub_token: bool = False) -> str:
    """
    Get the Discord bot token from the secrets file or keyring,
    and scrub it from the secrets file atomically using atomicwrites.

    :param scrub_token: Whether to scrub the token from the secrets file (currently not compatible with Docker build)
    :return: The Discord bot token
    """
    try:
        if SECRETS_JSON.is_file():
            loaded = json.loads(SECRETS_JSON.read_text())
            token = loaded[SERVICE_NAME][USERNAME]
            if scrub_token:
                loaded[SERVICE_NAME][USERNAME] = None
                with atomic_write(SECRETS_JSON, mode="w", overwrite=True) as f:
                    json.dump(loaded, f)
            return token
        # to store token: keyring.set_password(SERVICE_NAME, USERNAME, "<your token>")
        pw = keyring.get_password(SERVICE_NAME, USERNAME)
        if not isinstance(pw, str):
            raise RuntimeError("Token not found in keyring.")
        return pw
    except Exception as e:
        raise RuntimeError(f"Failed to obtain token:\n{e}")