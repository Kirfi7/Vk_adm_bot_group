import time

import vk_api
import gspread

from table import *
from cfg import TOKEN, SCOPE, DEV
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from oauth2client.service_account import ServiceAccountCredentials

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").sheet1


def sender(for_user_id, message_text):
    vk_session.method("messages.send", {"user_id": for_user_id, "message": message_text, "random_id": 0})


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {"chat_id": for_chat_id, "message": message_text, "random_id": 0})


def get_array(for_user_id):
    line_id = access(for_user_id)[0]
    values = sheet.row_values(line_id)
    values_array = list(values)
    return values_array


def get_keyboard():
    """получаю клавиатуру с дефолтными кнопками"""
    keyboard = VkKeyboard()
    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Ежедневная норма", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
    return keyboard


def access(from_user_id):
    """чекаю, есть ли юзер в адм-табле и определяю его строку"""
    ids = sheet.col_values(7)
    column_number = 0
    for i in ids:
        column_number += 1
        if str(i) == str(from_user_id):
            return column_number, 1
    return 0, 0


vk_session = vk_api.VkApi(token=TOKEN)
lp = VkLongPoll(vk_session)
vk = vk_session.get_api()

while True:
    try:
        for event in lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id

                if access(user_id)[1] == 1 and text == "Основная информация":
                    member_array = get_array(user_id)
                    sender(user_id, get_default_info(member_array))

                elif access(user_id)[1] == 1 and text == "Информация о повышениях":
                    member_array = get_array(user_id)
                    sender(user_id, get_info_about_rank(member_array))

                elif access(user_id)[1] == 1 and text == "Ежедневная норма":
                    member_array = get_array(user_id)
                    sender(user_id, get_rank_standard(member_array))

                elif event.text.lower() == "начать":
                    kb = get_keyboard()
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Создание кнопок...",
                        "random_id": 0,
                        "keyboard": kb.get_empty_keyboard()
                    })
                    time.sleep(0.25)
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Успешно!",
                        "random_id": 0,
                        "keyboard": kb.get_keyboard()
                    })

                # для фиксов и обновления кнопок
                elif event.text.lower() == "update_buttons" and user_id in DEV:
                    ids_column = sheet.col_values(7)
                    kb = get_keyboard()
                    for admin_id in ids_column:
                        try:
                            vk_session.method("messages.send", {
                                "user_id": admin_id,
                                "message": "Техническое пересоздание кнопок...",
                                "random_id": 0,
                                "keyboard": kb.get_empty_keyboard()
                            })
                            time.sleep(0.25)
                            vk_session.method("messages.send", {
                                "user_id": admin_id,
                                "message": "Успешно!",
                                "random_id": 0,
                                "keyboard": kb.get_keyboard()
                            })

                        except Exception as error:
                            sender(user_id, error)

    except Exception as error:
        chat_sender(1, error)
