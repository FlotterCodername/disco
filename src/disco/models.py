"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import hashlib
from contextlib import suppress
from datetime import UTC, datetime

import dateutil.parser
import feedparser
from dateutil.parser import parse
from django.db import models
from feedparser import FeedParserDict

from disco.configuration import Configurations
from disco.helpers import logger

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
    forward_guild = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    forward_channel = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    url_feed = models.URLField()
    url_artwork = models.URLField(null=True)
    date_cutoff = models.DateTimeField(default=datetime.fromtimestamp(0, tz=UTC))
    date_checked = models.DateTimeField(default=datetime.fromtimestamp(0, tz=UTC))
    date_updated = models.DateTimeField(default=datetime.fromtimestamp(0, tz=UTC))

    def get_feed(self) -> FeedParserDict:
        """
        Get a live copy of the feed

        :return: Feedparser dict
        """
        return feedparser.parse(self.url_feed)

    def update(self) -> None:
        """Update this podcast"""
        feed = self.get_feed()
        if feed.status != 200:
            return
        feed_data = feed.get("feed", {})
        self.name = feed_data.get("title", self.name)
        self.url_artwork = feed_data.get("image", {}).get("href", self.url_artwork)
        with suppress(KeyError, ValueError):
            self.date_updated = dateutil.parser.parse(feed["updated"])
        episodes = Episode.load_all(self, feed)
        if episodes:
            max_date = max(episodes, key=lambda e: e.date_published).date_published
            for episode in episodes:
                episode.save()
            self.date_cutoff = max_date
        self.date_checked = datetime.now(tz=UTC)
        self.save()

    @classmethod
    def make_id(cls, *, name: str) -> str:
        """
        ID factory

        :param name: Name of the podcast
        :return: ID for an instance
        """
        return generate_hash(name)

    @classmethod
    def load_from_configuration(cls) -> None:
        """Load all podcasts from the configuration into the DB"""
        configured = Configurations.podcasts.content["podcast"]
        for c in configured:
            podcast, created = cls.objects.get_or_create(id=cls.make_id(name=c["name"]), defaults=c)
            if created:
                logger.info(f"Added new podcast '{podcast.name}'")
            podcast.save()


class Episode(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    title = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    subtitle = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, null=True)
    summary = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, null=True)
    url_episode = models.URLField()
    url_artwork = models.URLField(null=True)
    date_published = models.DateTimeField()
    date_forwarded = models.DateTimeField(null=True)  #: When it was published to Discord
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    @classmethod
    def make_id(cls, *, url_episode: str, date_published: datetime) -> str:
        """
        ID factory

        :param url_episode: Title of the episode
        :param date_published: Date the episode was published
        :return: ID for an instance
        """
        return generate_hash(url_episode, date_published)

    @classmethod
    def load_all(cls, podcast: Podcast, from_feed: FeedParserDict | None) -> list["Episode"]:
        """
        Load all episodes for a podcast.

        :param podcast: Podcast to load episodes for
        :param from_feed: Cached copy of the podcast feed if available, otherwise fetch it
        :return: loaded episodes
        """
        # Load the XML file
        feed = from_feed or podcast.get_feed()
        # Extract episode information
        episodes = []
        for episode in feed.entries:
            if any(not episode.get(key) for key in {"title", "published", "link"}):
                logger.warning(f"Bad feed entry {episode=!s}")
            with suppress(ValueError):
                if (pub_date := parse(episode.get("published"))) <= podcast.date_cutoff:
                    continue
            if pub_date is None:
                logger.warning(f"Could not parse pub_date for {episode=!s}")
                continue
            episodes.append(
                Episode(
                    id=cls.make_id(url_episode=episode.get("link"), date_published=pub_date),
                    title=episode.get("title"),
                    subtitle=episode.get("subtitle") or None,
                    summary=episode.get("summary") or None,
                    url_episode=episode.get("link"),
                    url_artwork=episode.get("image", {}).get("href", podcast.url_artwork),
                    date_published=pub_date,
                    podcast=podcast,
                )
            )
        return episodes
