import requests


def http_get(**kwargs):
    response = requests.get(**kwargs)
    if response.status_code != 200:
        raise Exception(response.content)
    return response


__all__ = ["http_get"]
