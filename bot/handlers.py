from bot import bot, functions as f


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Начнем!")


@bot.message_handler(content_types=["location"])
def location_handler(message):
    location = message.location
    answer = f.create_answer("nearest_stations", (location.latitude, location.longitude))
    f.send_long_message(bot=bot,
                        chat_id=message.chat.id,
                        text=answer)


@bot.message_handler(func=lambda mess: f.is_search(mess.text.lower()),
                     content_types=["text"])
def search_handler(message):
    answer = f.create_answer("search", f.is_search(message.text.lower()).groups())
    f.send_long_message(bot=bot,
                        chat_id=message.chat.id,
                        text=answer)


@bot.message_handler(func=lambda mess: f.is_schedule(mess.text.lower()),
                     content_types=["text"])
def schedule_handler(message):
    answer = f.create_answer("schedule", f.is_schedule(message.text.lower()).groups())
    f.send_long_message(bot=bot,
                        chat_id=message.chat.id,
                        text=answer)


@bot.message_handler(func=lambda mess: True, content_types=["text"])
def other_text_handler(message):
    bot.reply_to(message=message,
                 text="Ты написал:")
