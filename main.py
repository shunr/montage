#!/usr/bin/env python3

import random

from montage import scraper
from montage import editor
from montage import settings

config = settings.load_config()

clips = scraper.get_videos(config["meta_tags"], 3)
random.shuffle(clips)
editor.generate_montage(clips, config["number_of_clips"])
