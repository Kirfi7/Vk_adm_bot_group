import time
import vk_api
import gspread
import config

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from oauth2client.service_account import ServiceAccountCredentials

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", config.SCOPE)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").worksheet("Успеваемость администрации")
punish = client.open("ADMINS RED1").worksheet("Логи выговоров")
vk_session = vk_api.VkApi(token=config.VK_TOKEN)


def sender(for_user_id, message_text):
    vk_session.method("messages.send", {"user_id": for_user_id, "message": message_text, "random_id": 0})


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {"chat_id": for_chat_id, "message": message_text, "random_id": 0})


def get_name(user_id):
    data = vk_session.method("users.get", {
        "user_ids": user_id,
        "name_case": "acc"
    })[0]
    return data["first_name"] + " " + data["last_name"]


def get_array(user_id) -> list:
    line_id = access(user_id)[0]
    values = sheet.row_values(line_id)
    values_array = list(values)
    return values_array


def get_keyboard(user_id):
    time.sleep(1)
    keyboard = VkKeyboard()
    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Последние наказания", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Инфа о повышении", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Связаться с ГА", VkKeyboardColor.NEGATIVE)
    vk_session.method("messages.send", {
        "user_id": user_id,
        "message": "Создание кнопок...",
        "random_id": 0,
        "keyboard": keyboard.get_empty_keyboard()
    })
    time.sleep(0.25)
    vk_session.method("messages.send", {
        "user_id": user_id,
        "message": "Успешно!",
        "random_id": 0,
        "keyboard": keyboard.get_keyboard()
    })


def send_report_message(user_id, message_id):
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button(label="Уведомить", payload={"type": "send", "msg": message_id}, color=VkKeyboardColor.PRIMARY)
    keyboard.add_callback_button(label="Отменить", payload={"type": "deny", "msg": message_id}, color=VkKeyboardColor.NEGATIVE)

    vk_session.method("messages.send", {
        "user_id": user_id,
        "message": config.report_message,
        "random_id": 0,
        "keyboard": keyboard.get_keyboard()
    })


def access(from_user_id):
    """Проверка, есть ли юзер в таблице и определение его строки"""
    ids = sheet.col_values(7)
    column_number = 0
    for j in ids:
        column_number += 1
        if str(j) == str(from_user_id):
            return column_number, 1
    return 0, 0


def editor(user_id, message_id, text):
    vk_session.method("messages.edit", {
        "conversation_message_id": message_id,
        "peer_id": user_id,
        "message": text
    })
