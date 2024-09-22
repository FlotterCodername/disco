"""
Copyright © 2024 Fabian H. Schneider

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from disco.models import Podcast

if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "disco.settings")

    # Create and save a podcast
    Podcast(
        name="Neue Zwanziger",
        url_feed="https://neuezwanziger.de/feed/mp3/",
        url_artwork="https://neuezwanziger.de/podcast/wp-content/uploads/2023/06/Zwanziger-Quadrat-3-1024x1024.jpg",
    ).save()
