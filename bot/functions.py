import re
import os
from datetime import date, timedelta
from bot import yarasp
from config import apikey
from telebot.apihelper import ApiException
from json import loads
from stations_list import all_stations


all_transport_types = {
    "самолет": "plane",
    "поезд": "train",
    "электричка": "suburban",
    "автобус": "bus",
    "морской транспорт": "water",
    "вертолет": "helicopter"
}

events = {"отправление": "departure", "прибытие": "arrival"}

emoji = {
    "plane": "\U00002708",
    "train": "\U0001F682",
    "suburban": "\U0001F683",
    "bus": "\U0001F68C",
    "water": "\U0001F6F3",
    "helicopter": "\U0001F681"
}


reg_event = "|".join(events.keys())
reg_transport = "|".join(all_transport_types.keys())
reg_city = "[а-я]+([- ](?!(сегодня|завтра|{transport}))[а-я]*)?".format(transport=reg_transport)
reg_date = "2018-((0[1-9]|1[012])-(0[1-9]|[12]\d)|(0[13-9]|1[012])-30|(0[13578]|1[02])-31)|завтра|сегодня"


def is_search(text):
    return re.match(
        # groups: 0, 3 7 -1
        "^({city}) — ({city})( ({date}))?( ({transport}))?$".format(
            city=reg_city, date=reg_date, transport=reg_transport
        ),
        text
    )


def is_schedule(text):
    return re.match(
        # groups: 0, 4, 11, -1
        "^({city})( ({date}))?( ({transport}))?( ({event}))?$".format(
            city=reg_city, date=reg_date, transport=reg_transport, event=reg_event
        ),
        text
    )


def get_code(title):
    # TODO delete bad search
    for c in all_stations["countries"]:
        if title == c["title"].lower():
            return c["codes"]["yandex_code"]
        else:
            for r in c["regions"]:
                if title == r["title"].lower():
                    return r["codes"]["yandex_code"]
                else:
                    for s in r["settlements"]:
                        if title == s["title"].lower():
                            return s["codes"]["yandex_code"]
                        else:
                            for st in s["stations"]:
                                if title == st["title"].lower():
                                    return st["codes"]["yandex_code"]
    return title


def get_date(text):
    if text == "сегодня":
        return date.today()
    elif text == "завтра":
        return date.today() + timedelta(days=1)
    else:
        return text


def create_answer(method, reg_groups):
    params = {"apikey": apikey}
    if method == "search":
        params["from"] = get_code(reg_groups[0])
        params["to"] = get_code(reg_groups[3])
        if reg_groups[7]:
            params["date"] = get_date(reg_groups[7])
        if reg_groups[-1]:
            params["transport_types"] = all_transport_types[reg_groups[-1]]
    elif method == "schedule":
        params["station"] = get_code(reg_groups[0])
        if reg_groups[4]:
            params["date"] = get_date(reg_groups[4])
        if reg_groups[11]:
            params["transport_types"] = all_transport_types[reg_groups[11]]
        if reg_groups[-1]:
            params["event"] = events[reg_groups[-1]]
    else:
        params["lat"] = reg_groups[0]
        params["lng"] = reg_groups[1]
        params["distance"] = 0.3
    return parse_ya_answer(method, yarasp.call(method, params))


def parse_ya_answer(method, ya_data):
    if "error" in ya_data:
        return "<b>Ошибка</b> при выполнении запроса к Яндекс.Расписанию: {0}".format(ya_data["error"]["text"])
    answer = ""
    if method == "search":
        for segment in ya_data["segments"]:
            answer += "{0} {1} <b>{2}</b> <i>({3})</i> - {4} <i>({5})</i> {6}\n\n".format(
                emoji[segment["thread"]["transport_type"]],
                segment["thread"]["number"],
                segment["departure"],
                segment["from"]["title"],
                segment["arrival"],
                segment["to"]["title"],
                segment["duration"]
            )
    elif method == "schedule":
        for schedule in ya_data["schedule"]:
            if schedule["departure"]:
                answer += "{0} {1} <b>{2}</b> {3}\n\n".format(
                    emoji[schedule["thread"]["transport_type"]],
                    schedule["thread"]["number"],
                    schedule["departure"],
                    schedule["thread"]["title"]
                )
            else:
                answer += "{0} {1} {2} <b>{3}</b>\n\n".format(
                    emoji[schedule["thread"]["transport_type"]],
                    schedule["thread"]["number"],
                    schedule["thread"]["title"],
                    schedule["arrival"]
                )
    else:
        for stations in ya_data["stations"]:
            answer += "{0} <b>{1}</b>, {2}\n\n".format(
                emoji[stations["transport_type"]],
                stations["title"],
                stations["station_type_name"],
            )
    return answer


def send_long_message(bot, chat_id, text, split="\n\n"):
    try:
        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode="HTML")
    except ApiException as e:
        json_err = loads(e.result.text)
        if json_err["description"] == "Bad Request: message is too long":
            event_count = len(text.split(split))
            first_part = split.join(text.split(split)[:event_count // 2])
            second_part = split.join(text.split(split)[event_count // 2:])
            send_long_message(bot, chat_id, first_part, split)
            send_long_message(bot, chat_id, second_part, split)


def create_stations_list():
    if os.path.exists("stations_list.py"):
        return
    else:
        all_stations = yarasp.call("stations_list", params={"apikey": apikey, "lang": "ru_RU"})
        with open("stations_list.py", "w") as f:
            f.write("all_stations = {0}".format(all_stations))
        print("stations_list.py created")
