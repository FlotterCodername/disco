"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from importlib.metadata import version

from packaging.version import Version, parse

__all__ = ["__product__", "__ua_header__", "__version__", "__version_obj__"]

__version__: str = version(__name__)
__version_obj__: Version = parse(__version__)
__product__: str = "discord-automation"
__ua_header__: dict = {"User-Agent": f"{__product__}/{__version__}"}
