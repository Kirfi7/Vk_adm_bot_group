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
# punish = client.open("ADMINS RED1").sheet2


def sender(for_user_id, message_text):
    vk_session.method("messages.send", {"user_id": for_user_id, "message": message_text, "random_id": 0})


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {"chat_id": for_chat_id, "message": message_text, "random_id": 0})


def get_array(for_user_id) -> list:
    line_id = access(for_user_id)[0]
    values = sheet.row_values(line_id)
    values_array = list(values)
    return values_array


def get_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Ежедневная норма", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
    return keyboard


def access(from_user_id):
    """Проверка, есть ли юзер в таблице и определение его строки"""
    ids = sheet.col_values(7)
    column_number = 0
    for j in ids:
        column_number += 1
        if str(j) == str(from_user_id):
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
                    message = get_info_about_rank(member_array)
                    if "✅" in message:
                        chat_sender(1, f"[id{user_id}|{member_array[1]}] достиг критерий для повышения")
                    sender(user_id, message)

                elif access(user_id)[1] == 1 and text == "Ежедневная норма":
                    member_array = get_array(user_id)
                    sender(user_id, get_rank_standard(member_array))

                elif access(user_id)[1] == 1 and text == "Начать":
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

                elif text == "update_buttons" and user_id in DEV:
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
                            sender(534422651, error)

                elif text == "ranked_up" and user_id in DEV:
                    all_ids = sheet.col_values(7)
                    ranked_array_1 = []
                    ranked_array_2 = []
                    ranked_array_3 = []
                    for admin_id in all_ids:
                        member_array = get_array(admin_id)
                        try:
                            rank_up = ranked_up(member_array)
                            if rank_up[0] == 1:
                                if rank_up[1][0] == "1":
                                    ranked_array_1.append(rank_up[1][1])
                                elif rank_up[1][0] == "2":
                                    ranked_array_2.append(rank_up[1][1])
                                else:
                                    ranked_array_3.append(rank_up[1][1])

                        except Exception as error:
                            sender(534422651, error)

                    m1 = "С Младшего Модератора на Модератора:"
                    m2 = "С Модератора на Администратора:"
                    m3 = "С Администратора на Старшего Администратора:"
                    for i1 in ranked_array_1:
                        m1 += f"{i1}\n"
                    for i2 in ranked_array_2:
                        m2 += f"{i2}\n"
                    for i3 in ranked_array_3:
                        m3 += f"{i3}\n"

                    chat_sender(1, f"Список допущенных к повышению:\n\n{m1}\n{m2}\n{m3}")

    except Exception as error:
        sender(534422651, error)
        sender(468509613, error)
