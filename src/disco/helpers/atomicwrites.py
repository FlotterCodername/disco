"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import contextlib
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from collections.abc import Generator

OpenTextMode = Literal[
    "r+",
    "+r",
    "rt+",
    "r+t",
    "+rt",
    "tr+",
    "t+r",
    "+tr",
    "w+",
    "+w",
    "wt+",
    "w+t",
    "+wt",
    "tw+",
    "t+w",
    "+tw",
    "a+",
    "+a",
    "at+",
    "a+t",
    "+at",
    "ta+",
    "t+a",
    "+ta",
    "x+",
    "+x",
    "xt+",
    "x+t",
    "+xt",
    "tx+",
    "t+x",
    "+tx",
    "w",
    "wt",
    "tw",
    "a",
    "at",
    "ta",
    "x",
    "xt",
    "tx",
    "r",
    "rt",
    "tr",
    "U",
    "rU",
    "Ur",
    "rtU",
    "rUt",
    "Urt",
    "trU",
    "tUr",
    "Utr",
]


@contextlib.contextmanager
def atomic_write(file_path: Path, mode: OpenTextMode = "w", overwrite: bool = False, **open_kwargs) -> Generator:
    """
    A context manager for atomic writing to a file. Reimplements atomicwrites.atomic_write from the `atomicwrites
    <https://github.com/untitaker/python-atomicwrites>`_ distribution.

    This creates a temporary file in the same directory as the target file and moves it to the final destination on
    successful write, ensuring atomicity.

    :param file_path: The target file path to write to atomically.
    :param mode: The mode to open the file in.
    :param overwrite: Raise an error if ``path`` exists. This error is only raised after the temporary has been written
                      to.
    :param open_kwargs: Additional keyword arguments passed to `open`.
    :returns: A writable file object.
    """
    with tempfile.NamedTemporaryFile(mode=mode, dir=file_path.parent, delete=False, **open_kwargs) as tmp_file:
        os_func = os.replace if overwrite else os.rename
        try:
            yield tmp_file
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            os_func(tmp_file.name, file_path)
        except Exception:
            Path(tmp_file.name).unlink()
            raise
