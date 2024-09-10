"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import hashlib
import html
import logging
from contextlib import suppress
from datetime import UTC, datetime

import requests
import xmltodict
from dateutil.parser import parse
from sqlalchemy import Column, DateTime, ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, relationship, sessionmaker

logger = logging.getLogger("discord")


Base: type[DeclarativeBase] = declarative_base()


class Podcast(Base):
    """Entity class for a podcast."""

    __tablename__ = "podcast"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    url_feed = Column(String, nullable=False)
    url_artwork = Column(String)

    def __init__(self, name: str, url_feed: str, url_artwork: str | None = None):
        """
        :param name: Official name of the podcast
        :param url_feed: URL to the podcast RSS feed
        :param url_artwork: URL to the podcast artwork (also fallback for episodes without artwork)
        """
        super().__init__()
        self.name = name
        self.url_feed = url_feed
        self.url_artwork = url_artwork
        self.id = hashlib.sha256(name.encode()).hexdigest()


class Episode(Base):
    """Entity class for an episode of a podcast."""

    __tablename__ = "episode"
    id = Column(String, primary_key=True)
    pub_date = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String)
    summary = Column(String)
    url_episode = Column(String)
    url_artwork = Column(String)
    podcast_id = Column(String, ForeignKey("podcast.id"), nullable=False)
    podcast = relationship("Podcast", back_populates="episodes")

    def __init__(
        self,
        pub_date: datetime,
        title: str,
        subtitle: str,
        summary: str,
        url_episode: str,
        url_artwork: str,
        podcast_id: str,
    ):
        """
        :param pub_date: Date and time of publication
        :param title: Title of the episode
        :param subtitle: Subtitle of the episode
        :param summary: Summary of the episode
        :param url_episode: URL to the episode (not the audio file)
        :param url_artwork: URL to the episode artwork
        :param podcast_id: ID of the podcast this episode belongs to
        """
        super().__init__()
        self.pub_date = pub_date
        self.title = title
        self.subtitle = subtitle
        self.summary = summary
        self.url_episode = url_episode
        self.url_artwork = url_artwork
        self.podcast_id = podcast_id
        self.id = hashlib.sha256(f"{pub_date.isoformat()}\x00{title}".encode()).hexdigest()

    @classmethod
    def load_all(cls, podcast: Podcast, from_date: datetime = datetime.fromtimestamp(0, tz=UTC)) -> list["Episode"]:
        """
        Load all episodes for a podcast.

        :param podcast: Podcast to load episodes for
        :param from_date: Load only episodes published after this date
        :return: loaded episodes
        """
        # Load the XML file
        data = xmltodict.parse(requests.get(podcast.url_feed).text)
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


Podcast.episodes = relationship("Episode", order_by=Episode.pub_date, back_populates="podcast")

# Database setup
engine = create_engine("sqlite:///podcasts.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    # Create and save a podcast
    _podcast = Podcast(
        name="Neue Zwanziger",
        url_feed="https://neuezwanziger.de/feed/mp3/",
        url_artwork="https://neuezwanziger.de/podcast/wp-content/uploads/2023/06/Zwanziger-Quadrat-3-1024x1024.jpg",
    )
    session.merge(_podcast)
    session.commit()

    # Load episodes and save them to the database
    _episodes = Episode.load_all(podcast=_podcast)
    for ep in _episodes:
        session.merge(ep)
    session.commit()
