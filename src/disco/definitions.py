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
    DISCO_HOME: str

    def __getattr__(self, item: str) -> str:
        """
        A simple getter that returns the attribute name regardless of whether it exists or not. Useful for getting
        defined attribute-like strings from the class.

        :param item: cf. official Python documentation
        :return: Name of the attribute
        """
        return item


EV = _Ev()
