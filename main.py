#!/usr/bin/env python3

from montage import scraper
from montage import editor
import random

META_TAGS = [
  "leagueoflegends:playerchampion:lucian",
  "leagueoflegends:event:pentakill"
]

N = 5
clips = scraper.get_videos(META_TAGS, 3)
random.shuffle(clips)
editor.generate_montage(clips[:N])
