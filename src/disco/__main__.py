"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import logging
import os
import sys

import discord
from discord.ext import commands

from disco.definitions import EV
from disco.helpers import get_discord_bot_token, get_log_handler

# Discord bot setup
logger = logging.getLogger("discord")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# This is a minimal bot logs in
@bot.event
async def on_ready():  # noqa RUF029
    logger.info(f"Logged in as {bot.user}")


if __name__ == "__main__":
    try:
        bot.run(token=get_discord_bot_token(), log_handler=get_log_handler())
    except Exception as e:
        if os.getenv(EV.DISCO_IS_DEBUG):
            print(f"An error occurred:\n{e}", file=sys.stderr)
        else:
            print("An error occurred.", file=sys.stderr)
        sys.exit(1)
