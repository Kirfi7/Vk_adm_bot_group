import time

import vk_api
import gspread

import cfg
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from oauth2client.service_account import ServiceAccountCredentials

# from pprint import pprint

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", cfg.SCOPE)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").sheet1

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
           f"\n🔑 Информация о повышении 🔑\n"


def get_info_about_rank(array):
    admin_lvl = array[12]
    reports = int(array[17]); up_date = int(array[18])
    p1 = array[14]; p2 = array[15]; p3 = array[16]

    rank_standards = {
        "1": {"days": 13, "reports": 4000},
        "2": {"days": 21, "reports": 8000},
        "3": {"days": 50, "reports": 25000}
    }

    if int(admin_lvl) < 4:
        days_by_lvl = rank_standards[admin_lvl]['days']
        reps_by_lvl = rank_standards[admin_lvl]['reports']

        if days_by_lvl > up_date and reps_by_lvl > reports:
            return cfg.rank_up_message(admin_lvl, (reps_by_lvl - reports), (reps_by_lvl - reports), p1, p2, p3, 0)

        elif days_by_lvl > up_date and reps_by_lvl <= reports:
            return cfg.rank_up_message(admin_lvl, 0, (days_by_lvl - up_date), p1, p2, p3, 0)

        elif days_by_lvl <= up_date and reps_by_lvl > reports:
            return cfg.rank_up_message(admin_lvl, (reps_by_lvl - reports), 0, p1, p2, p3, 0)

        else:
            return cfg.rank_up_message(admin_lvl, (reps_by_lvl - reports), 0, p1, p2, p3, 1)

    else:
        return "Достигнут максимальный админ-уровень!"

    # if (rank_up_message == "К повышению допущен(-а)!") and (int(array[14]) + int(array[15]) + int(array[16]) > 0):
    #     rank_up_message = "Имеются активные наказания!"
    #
    # default_massage = f"Ваш текущий уровень: {admin_lvl}\nДля повышения необходимо:\nОтветов — {} | Дней — {}"


vk_session = vk_api.VkApi(token=cfg.TOKEN)
lp = VkLongPoll(vk_session)
vk = vk_session.get_api()

while True:
    try:
        for event in lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id

                if access(user_id)[1] == 1 and text == "Основная информация":
                    line_id = access(user_id)[0]
                    row = sheet.row_values(line_id)
                    values_array = list(row)
                    sender(user_id, get_default_info(values_array))

                elif access(user_id)[1] == 1 and text == "Информация о повышениях":
                    line_id = access(user_id)[0]
                    row = sheet.row_values(line_id)
                    values_array = list(row)
                    sender(user_id, get_info_about_rank(values_array))

                elif event.text.lower() == "начать":
                    keyboard = VkKeyboard()
                    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
                    keyboard.add_line()
                    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Пересоздание кнопок...",
                        "random_id": 0,
                        "keyboard": keyboard.get_empty_keyboard()
                    })
                    time.sleep(1)
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Кнопки успешно созданы!",
                        "random_id": 0,
                        "keyboard": keyboard.get_keyboard()
                    })

                # для фиксов и переработки кнопок
                elif event.text.lower() == "full_reset_buttons" and user_id in cfg.DEV:
                    ids_column = sheet.col_values(7)
                    keyboard = VkKeyboard()
                    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
                    keyboard.add_line()
                    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
                    for admin_id in ids_column:
                        try:
                            vk_session.method("messages.send", {
                                "user_id": admin_id,
                                "message": "Загрузка обновления...",
                                "random_id": 0,
                                "keyboard": keyboard.get_empty_keyboard()
                            })
                            time.sleep(1)
                            vk_session.method("messages.send", {
                                "user_id": admin_id,
                                "message": "Кнопки были успелно обновлены\n\nЕсли с ними произошел баг, сообщите сюда: @xm_pearson\n\nБот временно не работает, исправится к вечеру",
                                "random_id": 0,
                                "keyboard": keyboard.get_keyboard()
                            })

                        except:
                            pass

    except Exception as error:
        chat_sender(1, error)
