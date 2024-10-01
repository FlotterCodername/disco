"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import json
import pathlib
import sys

__all__ = ["podcasts", "secrets"]


true, false, null = True, False, None

_base_uri = "https://raw.githubusercontent.com/FlotterCodername/disco/refs/heads/main/res/schemas"

podcasts = {
    "$id": f"{_base_uri}/podcasts.schema.v1.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "url-feed": {"type": "string", "format": "uri"},
        },
        "required": ["name", "url-feed"],
        "additionalProperties": false,
    },
}
secrets = {
    "$id": f"{_base_uri}/secrets.schema.v1.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "$schema": {"type": "string", "format": "uri"},
        "org.flottercodername.disco": {
            "type": "object",
            "properties": {"@@token": {"type": "string"}},
            "required": ["@@token"],
            "additionalProperties": false,
        },
    },
    "required": ["org.flottercodername.disco"],
    "additionalProperties": false,
}

_module_locals = locals()
_res_dir = pathlib.Path(__file__).parent.parent.parent / "res" / "schemas"


def _dump() -> int:
    """
    (Dev-only) Dump the schemas to the filesystem.

    :return: 0 if successful no changes were made, 1 otherwise
    """
    changed = 0
    schemas = [_module_locals[name] for name in __all__ if not name.startswith("_")]
    for schema in schemas:
        target = _res_dir / schema["$id"].removeprefix(f"{_base_uri}/")
        old_text = target.read_text() if target.is_file() else ""
        new_text = json.dumps(schema, indent=2) + "\n"
        if old_text != new_text:
            changed = 1
            target.write_text(new_text)
    return changed


if __name__ == "__main__":
    sys.exit(_dump())
