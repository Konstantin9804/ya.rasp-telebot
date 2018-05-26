import requests

api_url = "https://api.rasp.yandex.net/v3.0/{0}/"


def call(method, _from=None, **params):
    if _from:
        params["from"] = _from
    return requests.get(api_url.format(method), params=params).json()
