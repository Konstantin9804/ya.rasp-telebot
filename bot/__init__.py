import logging

from telebot import TeleBot, logger

from config import token

bot = TeleBot(token=token)

logger.setLevel(logging.INFO)


from bot import handlers
