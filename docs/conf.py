"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# mypy: ignore-errors

import datetime
import pathlib
import re
import tomllib

__pyproject = tomllib.load((pathlib.Path(__file__).parent.parent / "pyproject.toml").resolve().open("rb"))
__definitions = __pyproject.get("tool", {}).get("definitions", {})
__poetry = __pyproject.get("tool", {}).get("poetry", {})
__author_re = re.compile(r"(.+?) (<(.*?)>)")
__authors = [__author_re.match(i).group(1).strip() for i in __poetry.get("authors", [])]
__author_str = f"{", ".join(__authors[:-1])} and {__authors[-1]}".removeprefix(" and ")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = __definitions.get("name-pretty")
# noinspection PyShadowingBuiltins
copyright = f"{datetime.datetime.now().year}, {__author_str}"
author = __author_str
release = __poetry.get("version", "")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = __definitions.get("sphinx-extensions", [])
myst_enable_extensions = __definitions.get("myst-enable-extensions", [])

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = __definitions.get("sphinx-html-theme", "alabaster")
html_static_path = ["_static"]
