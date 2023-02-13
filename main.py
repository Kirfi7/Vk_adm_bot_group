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
           f"✅ Общее кол-во ответов: {array[17]}\n"


def get_info_about_rank(array):
    admin_lvl = array[12]

    rank_standards = {
        "1": {"days": 13, "reports": 4000, "this_rank": "Младшего Модератора", "next_rank": "Модератора"},
        "2": {"days": 21, "reports": 8000, "this_rank": "Модератора", "next_rank": "Администратора"},
        "3": {"days": 50, "reports": 25000, "this_rank": "Администратора", "next_rank": "Старшего Администратора"}
    }

    if int(admin_lvl) < 4:
        reports = int(array[17]); up_date = int(array[18])
        punish = [int(array[14]), int(array[15]), int(array[16])]
        t = f"С {rank_standards[admin_lvl]['this_rank']} на {rank_standards[admin_lvl]['next_rank']}:"

        days_by_lvl = int(rank_standards[admin_lvl]['days'])
        reps_by_lvl = int(rank_standards[admin_lvl]['reports'])

        if days_by_lvl > up_date and reps_by_lvl > reports:
            return cfg.rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), (days_by_lvl - up_date), punish, 0, t)

        elif days_by_lvl > up_date and reps_by_lvl <= reports:
            return cfg.rank_up(reps_by_lvl, days_by_lvl, 0, (days_by_lvl - up_date), punish, 0, t)

        elif days_by_lvl <= up_date and reps_by_lvl > reports:
            return cfg.rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punish, 0, t)

        else:
            return cfg.rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punish, 1, t)

    else:
        return "Достигнут максимальный админ-уровень!"


def get_rank_standard(get_admin):
    post = get_admin[0]
    second = get_admin[1]

    rank_standards = {
        "ММ": "Ответы: 250 штук\nОнлайн: 150 минут\nНаказаний: 10 штук",
        "М": "Ответы: 200 штук\nОнлайн: 150 минут\nНаказаний: 10 штук\nМероприятия: 2 штуки",
        "МК": "Ответы: 175 штук\nОнлайн: 150 минут\nНаказаний: 15 штук\nПост: За своей фракцией",
        "МФ": "Ответы: 150 штук\nОнлайн: 120 минут\nНаказаний: 10 штук\nФорум: 10 ответов\nМероприятия: 1 штука",
        "МК&МФ": "Ответы: 170 штук\nОнлайн: 150 минут\nНаказаний: 15 штук\nПост: За своей фракцией\nФорум: 10 ответов\nМероприятия: 1 штука",
        "А": "Ответы: 200 штук\nОнлайн: 150 минут\nНаказаний: 15 штук\nМероприятия: 2 штуки",
        "СА": "Ответы: 200 штук\nОнлайн: 150 минут\nНаказаний: 20 штук\nМероприятия: 1 штука",
        "ЗГС": "Ответы: 120 штук\nОнлайн: 130 минут\nНаказаний: 10 штук",
        "ГС": "Ответы: 100 штук\nОнлайн: 150 минут\nНаказаний: 5 штук",
        "К": "Ответы: 50 штук\nОнлайн: 150 минут"
    }

    if post == "Младший Модератор":
        standard = str(rank_standards['ММ'])
    elif second == "МФ":
        standard = str(rank_standards['МФ'])
    elif "МК" in second and "МФ" in second:
        standard = str(rank_standards['МК&МФ'])
    elif "МК" in second:
        standard = str(rank_standards['МК'])
    elif post == "Модератор":
        standard = str(rank_standards['М'])
    elif post == "Администратор ":
        standard = str(rank_standards['А'])
    elif post == "Старший Администратор":
        standard = str(rank_standards['СА'])
    elif "Заместитель Главного Следящего" in post:
        standard = str(rank_standards['ЗГС'])
    elif "Главный Следящий" in post:
        standard = str(rank_standards['ГС'])
    else:
        standard = str(rank_standards['К'])

    return f"Ваш ежедневный норматив:\n{standard}"


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
                    values = sheet.row_values(line_id)
                    values_array = list(values)
                    sender(user_id, get_default_info(values_array))

                elif access(user_id)[1] == 1 and text == "Информация о повышениях":
                    line_id = access(user_id)[0]
                    values = sheet.row_values(line_id)
                    values_array = list(values)
                    sender(user_id, get_info_about_rank(values_array))

                elif access(user_id)[1] == 1 and text == "Ежедневная норма":
                    line_id = access(user_id)[0]
                    values = sheet.row_values(line_id)
                    values_array = list(values)
                    sender(user_id, get_rank_standard([values_array[2], values_array[3]]))

                elif event.text.lower() == "начать":
                    keyboard = VkKeyboard()
                    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
                    keyboard.add_button("Ежедневная норма", VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Пересоздание кнопок...",
                        "random_id": 0,
                        "keyboard": keyboard.get_empty_keyboard()
                    })
                    time.sleep(0.25)
                    vk_session.method("messages.send", {
                        "user_id": user_id,
                        "message": "Кнопки успешно созданы!",
                        "random_id": 0,
                        "keyboard": keyboard.get_keyboard()
                    })

                # для фиксов и переработки кнопок
                elif event.text.lower() == "update_buttons" and user_id in cfg.DEV:
                    ids_column = sheet.col_values(7)
                    keyboard = VkKeyboard()
                    keyboard.add_button("Основная информация", VkKeyboardColor.POSITIVE)
                    keyboard.add_button("Ежедневная норма", VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button("Информация о повышениях", VkKeyboardColor.NEGATIVE)
                    for admin_id in ids_column:
                        try:
                            vk_session.method("messages.send", {
                                "user_id": admin_id,
                                "message": "Обновление кнопок...",
                                "random_id": 0,
                                "keyboard": keyboard.get_empty_keyboard()
                            })
                            time.sleep(0.25)
                            vk_session.method("messages.send", {
                                "user_id": admin_id,
                                "message": "Обновление успешно завершено!",
                                "random_id": 0,
                                "keyboard": keyboard.get_keyboard()
                            })

                        except:
                            pass

    except Exception as error:
        print(error)
