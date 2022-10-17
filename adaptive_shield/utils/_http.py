import requests

from adaptive_shield.errors import HttpGetError


def http_get(**kwargs):
    response = requests.get(**kwargs)
    if response.status_code != 200:
        raise HttpGetError(response.content)
    return response


__all__ = ["http_get"]
