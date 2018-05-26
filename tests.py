import unittest
import yarasp
from datetime import datetime, timedelta


apikey = ""


class YaRaspAPICase(unittest.TestCase):
    def test_search(self):
        """Расписание рейсов между станциями"""
        self.assertFalse(
            "error" in yarasp.call(
                "search", apikey=apikey, _from="c146", to="c213", lang="ru_RU", date=datetime.today()
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "search", apikey=apikey, _from="c146", to="c213", date=datetime.today() + timedelta(days=10), offset=15
            )
        )

    def test_schedule(self):
        """Расписание рейсов по станции"""
        self.assertFalse(
            "error" in yarasp.call(
                "schedule", apikey=apikey, station="s9600213", transport_types="suburban", direction="на Москву"
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "schedule", apikey=apikey, station="s9600213", transport_types="suburban", event="arrival"
            )
        )

    def test_nearest_stations(self):
        """Список ближайших станций"""
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_stations", apikey=apikey, format="json", lat=50.440046, lng=40.4882367, distance=50,
                lang="ru_RU"
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_stations", apikey=apikey, lat=59.887693, lng=30.268961, distance=20, offset=15,
                transport_types="plane"
            )
        )

    def test_nearest_settlement(self):
        """Ближайший город"""
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_settlement", apikey=apikey, format="json", lat=50.440046, lng=40.4882367, distance=50,
                lang="ru_RU"
            )
        )
        self.assertFalse(
            "error" in yarasp.call(
                "nearest_settlement", apikey=apikey, lat=59.887693, lng=30.268961, distance=20
            )
        )

    def test_copyright(self):
        """Копирайт Яндекс.Расписаний"""
        self.assertFalse(
            "error" in yarasp.call(
                "copyright", apikey=apikey, format="json"
            )
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
