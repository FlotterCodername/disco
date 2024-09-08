"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""


class _Ev:
    """Environment variable names."""

    DISCO_IS_DEBUG: str
    DISCO_IS_DOCKER: str
    DISCO_LOG: str
    DISCO_RUN: str

    def __getattr__(self, item: str) -> str:
        return item


EV = _Ev()

SERVICE_NAME = "org.flottercodername.disco"
USERNAME = "@@token"
