# mypy: ignore-errors
"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# based on: https://discordpy.readthedocs.io/en/stable/quickstart.html
import os
import re
import textwrap

import discord

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

RE_MINDSET = re.compile(r"mindset", re.IGNORECASE)
RE_RESILIENZ = re.compile(r"resilienz", re.IGNORECASE)


@client.event
def on_ready() -> None:
    """Logged in to Discord, let's log this very important event."""
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    """
    Respond to messages that contain 'mindset' or 'resilienz'.

    :param message: The message to (potentially) respond to
    """
    print(message, type(message))
    if message.author == client.user:
        return

    is_mindset = RE_MINDSET.search(message.content)
    is_resilienz = RE_RESILIENZ.search(message.content)

    if is_mindset and is_resilienz:
        await message.channel.send(
            "Da versucht wohl jemand, möglichst viele Hasswörter von Wolfgang M. Schmitt zu verwenden."
        )
    elif is_mindset:
        await message.channel.send(
            textwrap.dedent("""\
           "Wer Mindset sagt, hat den Verstand schon lange verloren."
           --Wolfgang M. Schmitt""")
        )
    elif is_resilienz:
        await message.channel.send(
            textwrap.dedent("""\
            "Wer Resilienz sagt, will betrügen."
            --Wolfgang M. Schmitt""")
        )


client.run(os.getenv("DISCORD_TOKEN"))
