"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import logging
import os
import pathlib
from importlib.metadata import version

import django
from packaging.version import Version, parse

__all__ = ["__product__", "__repo_root__", "__ua_header__", "__version__", "__version_obj__", "logger"]

__product__: str = "disco"
__version__: str = version(__product__)
__version_obj__: Version = parse(__version__)
__repo_root__ = pathlib.Path(__file__).parent.parent.parent  # incompatible with dists!
__ua_header__: dict = {"User-Agent": f"{__product__}/{__version__}"}

logger = logging.getLogger(__product__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "disco.settings")
django.setup()
