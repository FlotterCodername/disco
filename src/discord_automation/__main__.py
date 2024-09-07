"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import discord
import keyring
from discord.ext import commands

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# This is a minimal bot that logs in and immediately logs out


@bot.event
async def on_ready():
    await bot.close()


# to store token: keyring.set_password("org.flottercodername.disco", "@@token", "<your token>")
bot.run(keyring.get_password("org.flottercodername.disco", "@@token"))
