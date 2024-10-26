"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""


def deep_sort(data: dict | list) -> dict | list:
    """
    Recursively sort JSON-like structure by its keys and lists by their elements.

    :param data: JSON-like structure to sort
    :return: Sorted JSON-like structure
    """
    if isinstance(data, dict):
        # Sort dictionary by keys, recursively sort values
        return {k: deep_sort(v) for k, v in sorted(data.items())}
    if isinstance(data, list):
        # Sort list elements, which could be dicts or lists, or something else
        return [deep_sort(item) if isinstance(item, dict | list) else item for item in data]
    # Base case: return the item if it's neither a dict nor a list
    return data
