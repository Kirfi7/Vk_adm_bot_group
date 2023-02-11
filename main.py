import vk_api
import gspread

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from oauth2client.service_account import ServiceAccountCredentials

# from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").sheet1

DEV = [534422651, 468509613]

# row = sheet.row_values(3)
#
# data = sheet.get_all_records()  # Get a list of all records
#
# row = sheet.row_values(3)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell
#
# insertRow = ["hello", 5, "red", "blue"]
# sheet.add_rows(insertRow, 4)  # Insert the list as a row at index 4
#
# sheet.update_cell(2,2, "CHANGED")  # Update one cell
#
# numRows = sheet.row_count  # Get the number of rows in the sheet


def sender(for_user_id, message_text):
    vk_session.method("messages.send", {"user_id": for_user_id, "message": message_text, "random_id": 0})


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {"chat_id": for_chat_id, "message": message_text, "random_id": 0})


def access(from_user_id):
    ids_column = sheet.col_values(7)
    column_number = 0
    for i in ids_column:
        column_number += 1
        if str(i) == str(from_user_id):
            return column_number, 1
    return 0, 0


def get_default_info(array):

    if array[12] == "1":
        if int(array[19]) < 13 and int(array[17]) < 4000:
            rank_up_message = f"Дней до повышения: {13 - int(array[19])}" \
                              f"Ответов до повышения: {4000 - int(array[17])}"

        elif int(array[19]) >= 13 and int(array[17]) < 4000:
            rank_up_message = f"Ответов до повышения: {4000 - int(array[17])}"

        elif int(array[19]) < 13 and int(array[17]) >= 4000:
            rank_up_message = f"Дней до повышения: {13 - int(array[19])}"

        else:
            rank_up_message = "К повышению допущен(-а)!"

    elif array[12] == "2":
        if int(array[19]) < 21 and int(array[17]) < 8000:
            rank_up_message = f"Дней до повышения: {21 - int(array[19])}" \
                              f"Ответов до повышения: {8000 - int(array[17])}"

        elif int(array[19]) >= 21 and int(array[17]) < 8000:
            rank_up_message = f"Ответов до повышения: {8000 - int(array[17])}"

        elif int(array[19]) < 21 and int(array[17]) >= 8000:
            rank_up_message = f"Дней до повышения: {21 - int(array[19])}"

        else:
            rank_up_message = "К повышению допущен(-а)!"

    elif array[12] == "3":
        if int(array[19]) < 50 and int(array[17]) < 25000:
            rank_up_message = f"Дней до повышения: {50 - int(array[19])}\n" \
                              f"Ответов до повышения: {25000 - int(array[17])}"

        elif int(array[19]) >= 50 and int(array[17]) < 25000:
            rank_up_message = f"Ответов до повышения: {25000 - int(array[17])}"

        elif int(array[19]) < 50 and int(array[17]) >= 25000:
            rank_up_message = f"Дней до повышения: {50 - int(array[19])}"

        else:
            rank_up_message = "К повышению допущен(-а)!"

    else:
        rank_up_message = "Достигнут максимальный уровень!"

    if (rank_up_message == "К повышению допущен(-а)!") and (int(array[14]) + int(array[15]) + int(array[16]) > 0):
        rank_up_message = "Имеются активные наказания!"

    return f"🔑 Основная информация 🔑\n" \
           f"Ваш никнейм: {array[1]}\n" \
           f"Должность: {array[2]}\n" \
           f"Доп. должность: {array[3]}\n" \
           f"Уровень админ-прав: {array[12]}\n" \
           f"\n📅 Важные даты и дни 📅\n" \
           f"Дата постановки: {array[4]}\n" \
           f"Последнее повышение: {array[11]}\n" \
           f"Дней с момента повышения: {array[18]}\n" \
           f"Всего дней на админ-посту: {array[19]}\n" \
           f"\n⛔️ Активные наказания ⛔️\n" \
           f"Количество выговоров: {array[14]}/3\n" \
           f"Количество предов: {array[15]}/2\n" \
           f"Количество устных: {array[16]}/2\n\n" \
           f"✅ Общее кол-во ответов: {array[17]}\n" \
           f"\n🔑 Информация о повышении 🔑\n" \
           f"{rank_up_message}"


vk_session = vk_api.VkApi(token="vk1.a.RcpYvhXvj2P9NOfFXQ_ycHiFm1ENdqSKt4iRTR4_YltoNejArEwUNnQqy--Hq3vvyG_3-smfpgjNT-rHuUpNVcdJfMBRvV7CXhw0eL-T6dBYW-nAI1t_9834yfJpQBQaO1Y2Is9lRjDePfVEGwObaCyNOEWXaZL_K4OC9a7XXgbrpgGm-6vMOxShAufDs46qU34iqIervEGqItexmEX8nA")
lp = VkLongPoll(vk_session)
vk = vk_session.get_api()

while True:
    try:
        for event in lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id

                if access(user_id)[1] == 1 and text == "INFO":
                    line_id = access(user_id)[0]
                    row = sheet.row_values(line_id)
                    values_array = list(row)
                    sender(user_id, get_default_info(values_array))

                elif event.text.lower() == "начать":
                    keyboard = VkKeyboard()
                    keyboard.add_button("INFO", VkKeyboardColor.POSITIVE)
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Авторизация...",
                        "random_id": 0,
                        "keyboard": keyboard.get_empty_keyboard()
                    })
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Вы авторизовались в боте!",
                        "random_id": 0,
                        "keyboard": keyboard.get_keyboard()
                    })

                elif event.text.lower() == "full_reset_buttons" and user_id in DEV:
                    ids_column = sheet.col_values(7)
                    keyboard = VkKeyboard()
                    keyboard.add_button("INFO", VkKeyboardColor.POSITIVE)
                    for admin_id in ids_column:
                        try:
                            vk_session.method("messages.send", {
                                "user_id": user_id,
                                "message": "Тестовое сообщение 1",
                                "random_id": 0,
                                "keyboard": keyboard.get_empty_keyboard()
                            })
                            vk_session.method("messages.send", {
                                "user_id": user_id,
                                "message": "Тестовое сообщение 2",
                                "random_id": 0,
                                "keyboard": keyboard.get_keyboard()
                            })
                        except:
                            pass

    except Exception as error:
        chat_sender(1, error)
