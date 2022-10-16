import os
from adaptive_shield.utils import http_get
from bson import json_util


def get_main_page_image_url(title):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "pageimages|pageterms",
        "piprop": "original",
        "titles": title,
    }
    response = http_get(url=url, params=params)
    json_data = json_util.loads(response.text)
    pages = json_data["query"]["pages"]
    if not pages:
        return
    return pages[0].get("original", {}).get("source")


__all__ = ["get_main_page_image_url"]
