"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path

import jsonschema
import tomli_w

from disco.helpers.atomicwrites import atomic_write
from disco.paths import PODCASTS_TOML, SECRETS_TOML
from disco.schemas import podcasts, secrets


@dataclass
class _DcConfiguration:
    """One of the configurations for the application."""

    path: Path  #: The path to the configuration file.
    schema: dict  # The JSON schema for the configuration file.

    @property
    def exists(self) -> bool:
        """Check if the configuration file exists."""
        return self.path.is_file()

    @property
    def content(self) -> dict:
        """Load the configuration from the filesystem with validation."""
        if not self.exists:
            return {}
        loaded = tomllib.load(self.path.open("rb"))
        jsonschema.validate(loaded, self.schema)
        return loaded


class Configuration:
    """All configurations for the application."""

    podcasts = _DcConfiguration(PODCASTS_TOML, podcasts)
    secrets = _DcConfiguration(SECRETS_TOML, secrets)

    @classmethod
    def get_discord_bot_token(cls, scrub_token: bool = False) -> str:
        """
        Get the Discord bot token from the secrets file and scrub it from the secrets file atomically using
        atomicwrites.

        :param scrub_token: Whether to scrub the token from the config file (currently not compatible with Docker build)
        :return: The Discord bot token
        """
        try:
            if not Configuration.secrets.exists:
                raise RuntimeError(f"Missing configuration file at {Configuration.secrets.path}")
            loaded = Configuration.secrets.content
            token = loaded["disco"]["token"]
            if scrub_token:
                loaded["disco"]["token"] = None
                with atomic_write(SECRETS_TOML, mode="w", overwrite=True) as f:
                    tomli_w.dump(loaded, f)
            return token
        except Exception as e:
            raise RuntimeError(f"Failed to obtain token:\n{e}")
