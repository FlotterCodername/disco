"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os

import discord

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
def on_message(message: discord.Message):
    print(message, type(message))
    if message.author == client.user:
        return


client.run(os.getenv("DISCORD_TOKEN"))
