from bot import bot


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Начнем!")


@bot.message_handler(content_types=["location"])
def location_handler(message):
    location = message.location
    bot.reply_to(message=message,
                 text="Долгота: {0}\nШирота: {1}".format(location.longitude, location.latitude))


@bot.message_handler(func=lambda mess: True, content_types=["text"])
def other_text_handler(message):
    bot.reply_to(message=message,
                 text="Ты написал:")
