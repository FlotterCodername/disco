"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Literal

import tomli_w

from disco.helpers.sorting import deep_sort
from disco.paths import RES_SCHEMAS
from disco.schemas.docgen import JsonSchemaMarkdownGenerator

__all__ = ["bot", "podcasts", "secrets"]

_BASE_URI = "https://raw.githubusercontent.com/FlotterCodername/disco/refs/heads/main/res/schemas"
_DOC_GENERATOR = JsonSchemaMarkdownGenerator(indent_size=2)

true, false, null = True, False, None


@dataclass
class _DcSchema:
    name: str
    version: int
    _definition: dict  #: JSONSchema data
    _example: dict  #: Example TOML data

    @property
    def _id(self) -> str:
        """The schema ID."""
        return f"{_BASE_URI}/{self.name}.v{self.version}.schema.json"

    @property
    def example(self) -> dict:
        """Sorted example TOML data."""
        deep_sorted = deep_sort(self._example)
        if isinstance(deep_sorted, dict):
            return {"$schema": self._id} | deep_sorted
        raise TypeError

    @property
    def definition(self) -> dict:
        """Sorted JSONSchema data."""
        deep_sorted = deep_sort(self._definition)
        if isinstance(deep_sorted, dict):
            return {"$id": self._id, "$schema": "https://json-schema.org/draft/2020-12/schema"} | deep_sorted
        raise TypeError

    @property
    def markdown(self) -> str:
        """Markdown documentation of the schema."""
        return _DOC_GENERATOR.generate_markdown(self.definition)

    def get_path(self, suffix: Literal["md", "schema.json", "example.toml"]) -> pathlib.Path:
        """
        Get the path for the schema-related file.

        :param suffix: The file extension to append to the schema name.
        :return: The path to the file
        """
        return RES_SCHEMAS / f"{self.name}.v{self.version}.{suffix}"


bot = _DcSchema(
    "bot",
    1,
    {
        "additionalProperties": false,
        "description": "This configuration stores everything related to the bot itself.",
        "properties": {
            "$schema": {"description": "Which JSONSchema the file follows.", "format": "uri", "type": "string"},
            "no-reply": {
                "additionalProperties": false,
                "description": "Configuration for the 'no-reply' feature.",
                "properties": {
                    "enabled": {"description": "Whether the 'no-reply' feature is enabled.", "type": "boolean"},
                    "message": {
                        "description": (
                            "The message to send back when the bot receives a message. If empty or not set, a "
                            "default message in English will be sent."
                        ),
                        "type": "string",
                    },
                },
                "required": ["enabled"],
                "type": "object",
            },
        },
        "title": "Bot",
        "type": "object",
    },
    {
        "no-reply": {
            "enabled": true,
            "message": "⚠️ I am a bot. My inbox is not monitored.",
        }
    },
)

podcasts = _DcSchema(
    "podcasts",
    1,
    {
        "description": "This configuration stores everything related to podcast feeds.",
        "properties": {
            "$schema": {"description": "Which JSONSchema the file follows.", "format": "uri", "type": "string"},
            "podcast": {
                "description": "Podcast feeds to forward to a Discord channel.",
                "items": {
                    "additionalProperties": false,
                    "properties": {
                        "forward_channel": {
                            "description": "The exact name of the channel where podcast episodes shall appear.",
                            "type": "string",
                        },
                        "forward_guild": {
                            "description": (
                                "The exact name of the Discord server ('guild') where `forward_channel` is located."
                            ),
                            "type": "string",
                        },
                        "name": {
                            "description": (
                                "Your chosen name of the podcast (must be unique). May appear in user-facing text."
                            ),
                            "type": "string",
                        },
                        "url_artwork": {
                            "description": (
                                "The URL for the podcast cover art. This is also be used as a fallback whenever episode"
                                " artwork is not available."
                            ),
                            "format": "uri",
                            "type": "string",
                        },
                        "url_feed": {
                            "description": "The URL for the podcast RSS feed.",
                            "format": "uri",
                            "type": "string",
                        },
                    },
                    "required": ["name", "forward_guild", "forward_channel", "url_feed"],
                    "type": "object",
                },
                "type": "array",
            },
        },
        "title": "Podcasts",
        "type": "object",
    },
    {
        "podcast": [
            {
                "name": "My Podcast",
                "forward_channel": "podcast",
                "forward_guild": "My Server",
                "url_artwork": "https://example.com/podcast.jpg",
                "url_feed": "https://example.com/podcast.rss",
            },
            {
                "name": "My Other Podcast",
                "...": "...",
            },
        ]
    },
)

secrets = _DcSchema(
    "secrets",
    1,
    {
        "additionalProperties": false,
        "description": "This holds all the secrets required for your bot to function.",
        "properties": {
            "$schema": {"description": "Which JSONSchema the file follows.", "format": "uri", "type": "string"},
            "disco": {
                "additionalProperties": false,
                "description": "This holds all the actual secrets data.",
                "properties": {"token": {"description": "The 'Bot Token' from your Discord App.", "type": "string"}},
                "required": ["token"],
                "type": "object",
            },
        },
        "required": ["disco"],
        "title": "Secrets",
        "type": "object",
    },
    {"disco": {"token": "ABCDEFGHIJKLMNOPQRSTUVWXYZ.A1b2C3.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKL"}},
)

__locals = locals()


def _dump() -> int:
    """
    (Dev-only) Dump the schemas to the filesystem.

    :return: 0 if successful no changes were made, 1 otherwise
    """
    changed = 0
    schemas: list[_DcSchema] = [__locals[name] for name in __all__ if isinstance(__locals[name], _DcSchema)]
    for schema in schemas:
        # Schema
        target = schema.get_path("schema.json")
        old_text = target.read_text() if target.is_file() else ""
        new_text = json.dumps(schema.definition, indent=2) + "\n"
        if old_text != new_text:
            changed = 1
            target.write_text(new_text)
        # TOML example
        target = schema.get_path("example.toml")
        old_text = target.read_text("utf-8") if target.is_file() else ""
        new_text = tomli_w.dumps(schema.example, multiline_strings=True)
        if old_text != new_text:
            changed = 1
            target.write_text(new_text, "utf-8")
        # Markdown
        target = schema.get_path("md")
        old_text = target.read_text("utf-8") if target.is_file() else ""
        new_text = schema.markdown
        if old_text != new_text:
            changed = 1
            target.write_text(new_text, "utf-8")
    return changed


if __name__ == "__main__":
    sys.exit(_dump())
