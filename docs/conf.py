"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# mypy: ignore-errors

import datetime
import logging
import pathlib
import re
import tomllib

__pyproject = tomllib.load((pathlib.Path(__file__).parent.parent / "pyproject.toml").resolve().open("rb"))
__project = __pyproject.get("project", {})
__definitions = __pyproject.get("tool", {}).get("definitions", {})
__authors = [a.get("name", "").strip() for a in __project.get("authors", []) if a.get("name")]
__author_str = f"{', '.join(__authors[:-1])} and {__authors[-1]}".removeprefix(" and ") if __authors else ""

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = __definitions.get("name-pretty") or __project.get("name", "")
# noinspection PyShadowingBuiltins
copyright = f"{datetime.datetime.now().year}, {__author_str}".removesuffix(", ")
author = __author_str
release = __project.get("version", "")

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

# -- Processing ---------------------------------------------------------------
copyright_regex = re.compile(r"\bcopyright\b", re.IGNORECASE)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
def clear_copyright_docstring(app, what, name, obj, options, lines) -> None:
    """
    Event handler to replace module-level docstrings that have 'Copyright' in the first line (case-insensitive).

    :param app: The Sphinx application object
    :param what: The type of the object being documented (e.g., 'module', 'class', 'function')
    :param name: The name of the object
    :param obj: The actual object being documented
    :param options: The options given to the directive
    :param lines: The lines that make up the docstring
    """
    if what == "module" and lines and copyright_regex.match(lines[0]):
        lines.insert(0, "*No module description available.*")
        del lines[1:]


def setup(app) -> None:
    """
    Set up the Sphinx application object

    :param app: The Sphinx application object
    """
    app.connect("autodoc-process-docstring", clear_copyright_docstring)
