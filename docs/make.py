"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
import pathlib
import subprocess
import sys

# Abstract the make command for Windows and Unix systems

wd = pathlib.Path(__file__).parent.parent
if os.name == "nt":
    sp = subprocess.run([pathlib.Path(wd / "docs" / "make.bat"), *sys.argv[1:]], cwd=wd)
else:
    sp = subprocess.run(["make", *sys.argv[1:]], cwd=wd)
sys.exit(sp.returncode)
