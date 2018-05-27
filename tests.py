import unittest
from datetime import datetime, timedelta

from bot import yarasp, functions
from config import apikey


class YaRaspAPICase(unittest.TestCase):
    def test_search(self):
        """Запрос на Расписание рейсов между станциями"""
        self.assertFalse(
            "error" in yarasp.call(
                "search", params=dict(apikey=apikey, _from="c146", to="c213", lang="ru_RU", date=datetime.today())
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "search", params=dict(apikey=apikey, _from="c146", to="c213",
                                      date=datetime.today() + timedelta(days=10), offset=15)
            )
        )

    def test_schedule(self):
        """Запрос на Расписание рейсов по станции"""
        self.assertFalse(
            "error" in yarasp.call(
                "schedule", params=dict(apikey=apikey, station="s9600213", transport_types="suburban",
                                        direction="на Москву")
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "schedule", params=dict(apikey=apikey, station="s9600213", transport_types="suburban", event="arrival")
            )
        )

    def test_nearest_stations(self):
        """Запрос на Список ближайших станций"""
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_stations", params=dict(apikey=apikey, format="json", lat=50.440046, lng=40.4882367,
                                                distance=50, lang="ru_RU")
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_stations", params=dict(apikey=apikey, lat=59.887693, lng=30.268961, distance=20, offset=15,
                                                transport_types="plane")
            )
        )

    def test_nearest_settlement(self):
        """Запрос на Ближайший город"""
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_settlement", params=dict(apikey=apikey, format="json", lat=50.440046, lng=40.4882367,
                                                  distance=50, lang="ru_RU")
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_settlement", params=dict(apikey=apikey, lat=59.887693, lng=30.268961, distance=20)
            )
        )

    def test_copyright(self):
        """Запрос на Копирайт Яндекс.Расписаний"""
        self.assertFalse(
            "error" in yarasp.call(
                "copyright", params=dict(apikey=apikey, format="json")
            )
        )


class RegsCase(unittest.TestCase):
    def test_reg_search(self):
        """Парсинг для поиска маршрутов"""
        self.assertNotEqual(
            None,
            functions.is_search("Санкт-Петербург — Москва".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_search("Санкт-Петербург — Москва Завтра".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_search("Санкт-Петербург — Москва Самолет".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_search("Санкт-Петербург — Москва Завтра Самолет".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_search("Санкт-Петербург — Москва 2018-05-27".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_search("Санкт-Петербург — Нижний Новгород 2018-06-01 Поезд".lower())
        )

    def test_reg_schedule(self):
        """Парсинг для поиска расписания"""
        self.assertNotEqual(
            None,
            functions.is_schedule("Пулково 2018-06-03".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_schedule("Шереметьево электричка".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_schedule("Балтийский вокзал прибытие".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_schedule("Балтийский вокзал завтра отправление".lower())
        )
        self.assertNotEqual(
            None,
            functions.is_schedule("Шереметьево 2018-06-01 поезд отправление".lower())
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
