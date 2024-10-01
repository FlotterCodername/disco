"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import logging
from logging import handlers

import tomli_w

from disco import __product__
from disco.configuration import Configurations
from disco.helpers.atomicwrites import atomic_write
from disco.paths import DISCO_LOG, SECRETS_TOML


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
        if not Configurations.secrets.exists:
            raise RuntimeError(f"Missing configuration file at {Configurations.secrets.path}")
        loaded = Configurations.secrets.content
        token = loaded["disco"]["token"]
        if scrub_token:
            loaded["disco"]["token"] = None
            with atomic_write(SECRETS_TOML, mode="w", overwrite=True) as f:
                tomli_w.dump(loaded, f)
        return token
    except Exception as e:
        raise RuntimeError(f"Failed to obtain token:\n{e}")
