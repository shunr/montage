import requests

ENDPOINT = "https://plays.tv/ws/module"
ROOT_URL = "https://plays.tv"


def get_track(tags, max_pages):
    yield 1
