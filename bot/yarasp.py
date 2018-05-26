import requests

api_url = "https://api.rasp.yandex.net/v3.0/{0}/"


def call(method, params):
    _from = params.pop("_from", None)
    if _from:
        params["from"] = _from
    return requests.get(api_url.format(method), params=params).json()
