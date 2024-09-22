"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import hashlib
import html
from contextlib import suppress
from datetime import UTC, datetime

import requests
import xmltodict
from dateutil.parser import parse
from django.db import models

from disco import logger

CHAR_FIELD_MAX_LENGTH = 10 ^ 9  # Not enforced by SQLite


def generate_hash(*args) -> str:
    """
    Generate a hash from the provided arguments.

    :param args: Arguments to hash
    :return: Hash as hex string
    """
    hash_input = "".join(map(str, args)).encode("utf-8")
    return hashlib.sha256(hash_input).hexdigest()


class Podcast(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    url_feed = models.URLField()
    url_artwork = models.URLField(null=True)

    def save(self, *args, **kwargs) -> None:
        """
        Save the podcast.

        :param args: cf. Django
        :param kwargs: cf. Django
        """
        if not self.id:
            self.id = generate_hash(self.name)
        super().save(*args, **kwargs)


class Episode(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    subtitle = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, null=True)
    summary = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, null=True)
    url_episode = models.URLField()
    url_artwork = models.URLField(null=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    def save(self, *args, **kwargs) -> None:
        """
        Save the podcast episode.

        :param args: cf. Django
        :param kwargs: cf. Django
        """
        if self.id:
            self.id = generate_hash(self.pub_date)
        super().save(*args, **kwargs)

    @classmethod
    def load_all(cls, podcast: Podcast, from_date: datetime = datetime.fromtimestamp(0, tz=UTC)) -> list["Episode"]:
        """
        Load all episodes for a podcast.

        :param podcast: Podcast to load episodes for
        :param from_date: Load only episodes published after this date
        :return: loaded episodes
        """
        # Load the XML file
        data = xmltodict.parse(requests.get(podcast.url_feed).text)  # todo adjust to django model
        # Extract episode information
        episodes = []
        for episode in data.get("rss", {}).get("channel", {}).get("item", []):
            with suppress(ValueError):
                if (pub_date := parse(episode.get("pubDate"))) < from_date:
                    continue
            if pub_date is None:
                logger.warning(f"Could not parse pub_date for {episode=!s}")
            episodes.append(
                Episode(
                    pub_date=pub_date,
                    title=episode.get("title", "?"),
                    subtitle=episode.get("itunes:subtitle"),
                    summary=html.unescape(episode.get("itunes:summary")) if episode.get("itunes:summary") else None,
                    url_episode=episode.get("link"),
                    url_artwork=episode.get("itunes:image", {}).get("@href", podcast.url_artwork),
                    podcast_id=podcast.id,
                )
            )
        # Sort the episodes by pub_date in ascending order
        return sorted(episodes, key=lambda _ep: _ep.pub_date)
