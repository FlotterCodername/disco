"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import discord
from discord.ext import commands

from disco.helpers import get_discord_bot_token

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# This is a minimal bot that logs in and immediately logs out


@bot.event
async def on_ready():
    await bot.close()


bot.run(get_discord_bot_token())
