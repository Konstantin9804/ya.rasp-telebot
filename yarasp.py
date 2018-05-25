import requests

api_url = "https://api.rasp.yandex.net/v3.0/{0}/"


def call(method, **params):
    return requests.get(api_url.format(method), params=params).json()
