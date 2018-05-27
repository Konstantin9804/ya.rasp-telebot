from bot import bot, functions as f


if __name__ == "__main__":
    f.create_stations_list()
    bot.polling()
