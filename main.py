import time

import vk_api
import gspread

from cfg import TOKEN, SCOPE, ACCESS, CMDS
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from oauth2client.service_account import ServiceAccountCredentials
from table import get_default_info, get_info_about_rank, punishment

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").worksheet("Успеваемость администрации")
punish = client.open("ADMINS RED1").worksheet("Логи выговоров")


def sender(for_user_id, message_text):
    vk_session.method("messages.send", {"user_id": for_user_id, "message": message_text, "random_id": 0})


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {"chat_id": for_chat_id, "message": message_text, "random_id": 0})


def get_array(for_user_id) -> list:
    line_id = access(for_user_id)[0]
    values = sheet.row_values(line_id)
    values_array = list(values)
    return values_array


def get_keyboard(for_user_id):
    keyboard = VkKeyboard()
    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Последние наказания", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
    vk_session.method("messages.send", {
        "user_id": for_user_id,
        "message": "Создание кнопок...",
        "random_id": 0,
        "keyboard": keyboard.get_empty_keyboard()
    })
    time.sleep(0.25)
    vk_session.method("messages.send", {
        "user_id": for_user_id,
        "message": "Успешно!",
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


vk_session = vk_api.VkApi(token=TOKEN)
lp = VkLongPoll(vk_session)
vk = vk_session.get_api()

while True:
    try:
        for event in lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id
                is_access = access(user_id)

                if is_access[1] != 1:
                    continue

                nick_name = sheet.cell(is_access[0], 2).value

                if text == "Начать":
                    get_keyboard(user_id)

                if text == "Основная информация":
                    member_array = get_array(user_id)
                    sender(user_id, get_default_info(member_array))

                if text == "Последние наказания":
                    sender(user_id, "Последние 10 действий с наказаниями:\n\n" + punishment(nick_name))

                if text == "Информация о повышениях":
                    member_array = get_array(user_id)
                    message = get_info_about_rank(member_array)
                    sender(user_id, message)

                cmd = text[1:]
                if text[0] in ["/", "!", "+"] and cmd.split()[0] in CMDS:

                    if cmd == "update" and user_id in ACCESS:
                        all_admins = list(set(sheet.col_values(7)))[2:]
                        [get_keyboard(admin) for admin in all_admins]
                        continue

                    array = cmd.split()
                    if len(array) == 0:
                        sender(user_id, "Введите команду повторно, указав никнейм админа.")
                        continue

                    if "punish" in cmd:
                        argument = array[1]
                        sender(user_id, punishment(argument, is_big=True))

    except:
        pass
