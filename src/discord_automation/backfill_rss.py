"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from dataclasses import dataclass
from pathlib import Path

import discord
import keyring
import xmltodict
from discord.ext import commands
from discord.utils import get

from discord_automation import __repo_root__


@dataclass
class Episode:
    title: str
    subtitle: str
    link: str
    artwork: str

    @classmethod
    def load_all(cls):
        # Load the XML file
        data = xmltodict.parse((Path(__repo_root__) / "res" / "neuezwanziger.xml").read_bytes())
        # Extract episode information
        episodes = []
        for item in data.get("rss", {}).get("channel", {}).get("item", []):
            title = item["title"]
            subtitle = item.get("itunes:subtitle", None)
            link = item.get("link", None)
            artwork = item.get("itunes:image", {}).get(
                "@href", "https://neuezwanziger.de/podcast/wp-content/uploads/2023/06/Zwanziger-Quadrat-3-1024x1024.jpg"
            )
            episodes.append(Episode(title, subtitle, link, artwork))
            print(episodes[-1].artwork)
        # Reverse the list to send older episodes first
        episodes.reverse()
        return episodes


EPISODES = Episode.load_all()


# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    guild_name = "Inoffizielle NZ Testumgebung"  # Replace with your guild name
    channel_name = "rss-feeds"  # Replace with your channel name
    tryout = True
    counter = 0
    for guild in bot.guilds:
        if guild.name == guild_name:
            channel = get(guild.channels, name=channel_name)
            if channel:
                print(f"Channel ID for {channel_name}: {channel.id}")
                for ep in EPISODES:
                    if tryout and counter > 3:
                        break
                    embed = discord.Embed(title=ep.title, description=ep.subtitle, url=ep.link)
                    embed.set_image(url=ep.artwork)
                    await channel.send(embed=embed)
                    counter += 1
                break
            print(f"Channel {channel_name} not found in guild {guild_name}")
            break
    else:
        print(f"Guild {guild_name} not found")

    await bot.close()


# to store: keyring.set_password("org.flottercodername.disco", "@@token", "<your token>")
bot.run(keyring.get_password("org.flottercodername.disco", "@@token"))
