"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import asyncio
import os
import sys
import textwrap
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks
from discord.utils import get

from disco.definitions import EV
from disco.helpers import get_discord_bot_token, get_log_handler, logger
from disco.helpers.database import bootstrap
from disco.models import Episode, Podcast

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from discord.guild import GuildChannel

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(minutes=5)
async def synchronize_podcasts() -> None:
    """Synchronize podcasts every 5 minutes."""
    logger.info("Synchronizing podcasts...")

    def sync_get_podcasts() -> list[Podcast]:
        _podcasts: list[Podcast] = Podcast.objects.all()
        for _podcast in _podcasts:
            logger.info(f"Syncing podcast: {_podcast.name}")
            _podcast.update()
        return _podcasts

    podcasts = await asyncio.to_thread(sync_get_podcasts)

    def sync_get_episodes(_podcast: Podcast) -> list[Episode]:
        return [*Episode.objects.filter(date_forwarded=None, podcast=_podcast).order_by("date_published")]

    for podcast in podcasts:
        episodes: list[Episode] = await asyncio.to_thread(sync_get_episodes, podcast)
        channel = None
        guild = None
        for _guild in bot.guilds:
            guild = _guild if _guild.name == podcast.forward_guild else guild
            if guild:
                channel = get(guild.channels, name=podcast.forward_channel)
                break
        if not guild:
            logger.warning(f"Guild {podcast.forward_channel} not found")
        if guild and not channel:
            logger.warning(f"Channel {podcast.forward_channel} not found in guild {guild}")
        if channel:
            logger.info(f"Channel ID for {podcast.forward_channel}: {channel.id}")
            await _publish_episodes(podcast, episodes, channel)


async def _publish_episodes(podcast: Podcast, episodes: list[Episode], channel: "GuildChannel") -> None:
    """
    McCabe complexity reduction for the `synchronize_podcasts` task.

    :param podcast: Podcast with the episodes
    :param episodes: The episodes to publish
    :param channel: The channel to publish to
    """

    def sync_update_episode(_episode: Episode) -> None:
        _episode.date_forwarded = datetime.now(tz=UTC)
        _episode.save()

    for episode in episodes:
        logger.info(f"Publishing episode from {episode.date_published}: '{episode.title}'")
        embed = discord.Embed(
            title=episode.title,
            url=episode.url_episode,
            description=textwrap.shorten(episode.subtitle or episode.summary, 240),
            timestamp=episode.date_published,
        )
        embed.set_image(url=episode.url_artwork)
        message = await channel.send(f"📣 **{podcast.name.replace("*", r"\*")}**", embed=embed)
        logger.info(f"Sent message: {message}")
        await asyncio.to_thread(sync_update_episode, episode)


@bot.event
async def on_ready() -> None:  # noqa RUF029
    """Logged in to Discord, let's log this very important event."""
    logger.info(f"Logged in as {bot.user}")
    synchronize_podcasts.start()


def main() -> int:
    """
    Entry point for the Discord bot.

    :return: exit code
    """
    try:
        bootstrap()
        bot.run(token=get_discord_bot_token(), log_handler=get_log_handler("bot"))
    except Exception as e:
        if os.getenv(EV.DISCO_IS_DEBUG):
            print(f"An error occurred:\n{e}", file=sys.stderr)
        else:
            print("An error occurred.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
