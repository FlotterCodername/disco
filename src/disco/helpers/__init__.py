"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import logging
from logging import StreamHandler, handlers

from disco import __product__
from disco.paths import DISCO_LOG


def get_log_handler(suffix: str) -> handlers.RotatingFileHandler:
    """
    Configure the logging for the bot (taken from `discord.py docs
    <https://discordpy.readthedocs.io/en/v2.4.0/logging.html>`_.)

    :param suffix: The suffix for the log file
    :return: The logging handler
    """
    DISCO_LOG.mkdir(parents=True, exist_ok=True)
    handler = handlers.RotatingFileHandler(
        filename=DISCO_LOG / f"{__product__}-{suffix}.log", encoding="utf-8", maxBytes=32 * 1024 * 1024, backupCount=5
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    handler.setFormatter(formatter)
    return handler


logger = logging.getLogger(__product__)
logger.setLevel(10)
logger.addHandler(get_log_handler("app"))
logger.addHandler(StreamHandler())
