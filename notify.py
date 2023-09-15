from telebot import TeleBot
from config import TG_TOKEN

tg_session = TeleBot(token=TG_TOKEN)


def send_notify(admin_id, admin_name):
    tg_session.send_message(777198928, f"Пришел запрос от {admin_name}:\nhttps://vk.com/id{admin_id}")
