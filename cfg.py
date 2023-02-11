TOKEN = "vk1.a.RcpYvhXvj2P9NOfFXQ_ycHiFm1ENdqSKt4iRTR4_YltoNejArEwUNnQqy--Hq3vvyG_3-smfpgjNT-rHuUpNVcdJfMBRvV7CXhw0eL-T6dBYW-nAI1t_9834yfJpQBQaO1Y2Is9lRjDePfVEGwObaCyNOEWXaZL_K4OC9a7XXgbrpgGm-6vMOxShAufDs46qU34iqIervEGqItexmEX8nA"

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

DEV = [534422651, 468509613]

default_text = "Чтобы попасть в список на повышение не надо никому писать, в нужное время вы будете добавлены автоматически."


def rank_up_message(admin_lvl, reps, days, p1, p2, p3, x) -> str:
    if x == 0:
        return f"🔑 Информация о повышениях 🔑\n\nВаш текущий админ-уровень: {admin_lvl}\n\n" \
               f"Чтобы получить повышение, необходимо отстоять {days} дней, \n" \
               f"накопить {reps} ответов и не иметь активных наказаний.\n\n{default_text}\n\n" \
               f"Ваша статистика на данный момент:\nОсталось ответов — {reps}\n" \
               f"Осталось дней — {days}\n\nВыговоров: {p1}/3\nПредупреждений: {p2}/2\nУстных выговоров: {p3}/2"

    else:
        return f"Вы выполнили все критерии для получения повышения!\n\n{default_text}"
