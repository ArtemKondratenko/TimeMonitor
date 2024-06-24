from telegram import Bot
import telebot
from model.monitor import MonitorInDB


def message_tg_bot(apitgBot: str, chat_id: int,  monitor: MonitorInDB, status_code: int):
    bot = telebot.TeleBot(apitgBot)
    message = f"Monitor {monitor.url} failed with status code { status_code}"
    bot.send_message(chat_id=chat_id, text=message)