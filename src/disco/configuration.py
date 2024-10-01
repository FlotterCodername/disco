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

from disco.paths import PODCASTS_TOML, SECRETS_TOML
from disco.schemas import podcasts, secrets


@dataclass
class Configuration:
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
        loaded = tomllib.load(self.path.open("rb"))
        jsonschema.validate(loaded, self.schema)
        return loaded


class Configurations:
    """All configurations for the application."""

    podcasts = Configuration(PODCASTS_TOML, podcasts)
    secrets = Configuration(SECRETS_TOML, secrets)
