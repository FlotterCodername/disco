"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import json
import pathlib
import sys

from disco.helpers.sorting import deep_sort

__all__ = ["podcasts", "secrets"]

from disco.schemas.docgen import dump_markdown_docs

true, false, null = True, False, None

_base_uri = "https://raw.githubusercontent.com/FlotterCodername/disco/refs/heads/main/res/schemas"

podcasts = {
    "$id": f"{_base_uri}/podcasts.schema.v1.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "properties": {
        "$schema": {"format": "uri", "type": "string"},
        "podcast": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "forward_channel": {"type": "string"},
                    "forward_guild": {"type": "string"},
                    "name": {"type": "string"},
                    "url_artwork": {"format": "uri", "type": "string"},
                    "url_feed": {"format": "uri", "type": "string"},
                },
                "required": ["name", "forward_guild", "forward_channel", "url_feed"],
                "type": "object",
            },
            "type": "array",
        },
    },
    "type": "object",
}

secrets = {
    "$id": f"{_base_uri}/secrets.schema.v1.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "additionalProperties": false,
    "properties": {
        "$schema": {"format": "uri", "type": "string"},
        "disco": {
            "additionalProperties": false,
            "properties": {"token": {"type": "string"}},
            "required": ["token"],
            "type": "object",
        },
    },
    "required": ["disco"],
    "type": "object",
}


_module_locals = locals()
_res_dir = pathlib.Path(__file__).parent.parent.parent.parent / "res" / "schemas"


def _dump() -> int:
    """
    (Dev-only) Dump the schemas to the filesystem.

    :return: 0 if successful no changes were made, 1 otherwise
    """
    changed = 0
    schemas = [_module_locals[name] for name in __all__ if not name.startswith("_")]
    for schema in schemas:
        # Schema
        target = _res_dir / schema["$id"].removeprefix(f"{_base_uri}/")
        old_text = target.read_text() if target.is_file() else ""
        new_text = json.dumps(deep_sort(schema), indent=2) + "\n"
        if old_text != new_text:
            changed = 1
            target.write_text(new_text)
        # Markdown
        target = target.with_suffix(".md")
        old_text = target.read_text() if target.is_file() else ""
        new_text = dump_markdown_docs(schema)
        if old_text != new_text:
            changed = 1
            target.write_text(new_text)
    return changed


if __name__ == "__main__":
    sys.exit(_dump())
