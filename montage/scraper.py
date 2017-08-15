import requests
from bs4 import BeautifulSoup
from montage.classes.montage_clip import MontageClip

ENDPOINT = "https://plays.tv/ws/module"
ROOT_URL = "https://plays.tv"

PARAMS = {
    "sort": "sort_popular",
    "game_id": "b179585c6b68a2791eea4a1ad3d7ef72",
    "format": "application/json",
    "id": "FilterVideosMod"
}


def get_videos(tags, max_pages):
    videos = []
    for i in range(max_pages):
        request_string = ENDPOINT + "?page=" + str(i + 1)
        for param, val in PARAMS.items():
            request_string += ("&" + param + "=" + val)
        request_string += "&metatags=" + ",".join(tags)
        page = _parse_page(requests.get(request_string).json()["body"])
        if page is None:
            break
        for video in page:
            videos.append(video)
    return videos


def _parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(class_="video-item")
    if not elements:
        return None
    for element in elements:
        yield _parse_video(element)


def _parse_video(element):
    title = element.find(class_="title").get_text()
    author = element.find(class_="author").find("strong").get_text()
    link = ROOT_URL + element.find(class_="title").get("href")
    src = "https:" + \
        element.find("video").find("source").get(
            "src").replace("preview_144", "720")
    video = MontageClip(title, author, link, src)
    return video
