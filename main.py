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
data = sheet.get_all_values()

# cola = sheet.col_values(14)
# col = sheet.col_values(2)
# cole = sheet.col_values(15)
# coli = sheet.col_values(16)

# row = sheet.row_values(3)

# pprint(row[:17])
# pprint(col+cola+cole+coli)

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
# numRows = sheet.row_count  # Get the number of rows in the sheetuioouiuiouiopuiopuio


def sender(for_user_id, message_text):
    vk_session.method("messages.send", {"user_id": for_user_id, "message": message_text, "random_id": 0})


def access(from_user_id):
    ids_column = sheet.col_values(7); column_number = 0
    for i in ids_column:
        column_number += 1
        if str(i) == str(from_user_id):
            return column_number, 1
    return 0, 0


def get_default_info(array):
    nick_name = array[1]
    date = array[4]
    admin_post = array[2]
    alt_admin_post = array[3]
    rank_up_date = array[11]
    admin_level = array[12]
    reports = array[17]
    days_by_rank_up = array[18]
    days_by_date = array[-5]
    punish_1 = array[14]
    punish_2 = array[15]
    punish_3 = array[16]


    if admin_post == "Младший Модератор" or admin_level < "4":
        ranked_up = "Допущен" if (int(reports) >= 4000 and int(days_by_rank_up >= 13)) else "Отсутствует"

    elif admin_post == "Модератор" or admin_level < "4":
        ranked_up = "Допущен" if (int(reports) >= 8000 and int(days_by_rank_up >= 21)) else "Отсутствует"

    elif admin_post == "Администратор" or admin_level < "4":
        ranked_up = "Допущен" if (int(reports) >= 25000 and int(days_by_rank_up >= 50)) else "Отсутствует"

    else:
        ranked_up = "Максимальный уровень"

    return f"🔑 Основная информация 🔑\n" \
           f"Ваш никнейм: {nick_name}\n" \
           f"Должность: {admin_post}\n" \
           f"Доп. должность: {alt_admin_post}\n" \
           f"Уровень админ-прав: {admin_level}\n" \
           f"\n📅 Важные даты и дни 📅\n" \
           f"Дата постановки: {date}\n" \
           f"Дата повышения: {rank_up_date}\n" \
           f"Дней с повышения: {days_by_rank_up}\n" \
           f"Дней на админ-посту: {days_by_date}\n" \
           f"\n⛔️ Активные наказания ⛔️\n" \
           f"Количество выговоров: {punish_1}\n" \
           f"Количество предов: {punish_2}\n" \
           f"Количество устных: {punish_3}\n\n" \
           f"✅ Общее кол-во ответов: {reports}\n" \
           f"Допуск к повышению: {ranked_up}\n"


prefix = ["/", "!", "+"]

vk_session = vk_api.VkApi(token="vk1.a.RcpYvhXvj2P9NOfFXQ_ycHiFm1ENdqSKt4iRTR4_YltoNejArEwUNnQqy--Hq3vvyG_3-smfpgjNT-rHuUpNVcdJfMBRvV7CXhw0eL-T6dBYW-nAI1t_9834yfJpQBQaO1Y2Is9lRjDePfVEGwObaCyNOEWXaZL_K4OC9a7XXgbrpgGm-6vMOxShAufDs46qU34iqIervEGqItexmEX8nA")
lp = VkLongPoll(vk_session)
vk = vk_session.get_api()


for event in lp.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text
        user_id = event.user_id

        if access(user_id)[1] != 0 and text == "INFO":
            line_id = access(user_id)[0]
            row = sheet.row_values(line_id)
            values_array = list(row)
            sender(user_id, get_default_info(values_array))

        elif event.text.lower() == "начать":
            keyboard = VkKeyboard()
            keyboard.add_button("INFO", VkKeyboardColor.POSITIVE)
            vk_session.method("messages.send", {
                "user_id": user_id,
                "message": "Вы авторизовались в боте!",
                "random_id": 0,
                "keyboard": keyboard.get_keyboard()
            })
