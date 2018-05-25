import logging

from telebot import TeleBot, logger


token = "610309510:AAEglz7qsg10XIuauvXKEQvufPanQ9zPQeo"
bot = TeleBot(token=token)

logger.setLevel(logging.INFO)


from bot import handlers
