VK_TOKEN = "vk1.a.RcpYvhXvj2P9NOfFXQ_ycHiFm1ENdqSKt4iRTR4_YltoNejArEwUNnQqy--Hq3vvyG_3-smfpgjNT-rHuUpNVcdJfMBRvV7CXhw0eL-T6dBYW-nAI1t_9834yfJpQBQaO1Y2Is9lRjDePfVEGwObaCyNOEWXaZL_K4OC9a7XXgbrpgGm-6vMOxShAufDs46qU34iqIervEGqItexmEX8nA"
TG_TOKEN = "6331677615:AAHOeIYrTSRFGGbzjwsI0oYd4qJhsEHvlow"

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

ACCESS = {534422651: "Миша", 468509613: "Кирилл", 16715256: "Прохор", 345814069: "Костя"}

CMDS = ["punish", "remove", "update", "global"]


def rank_up(full_reps: int, full_days: int, reps: int, days: int, punish: list, x: int, t: str) -> str:
    """Функция для форматирования ответа на запрос об информации по повышению"""
    if (x == 0) or ((punish[0] + punish[1] + punish[2]) != 0):
        return f"🔑 Информация о повышениях 🔑\n\n{t}\n" \
               f"Отстоять {full_days} дней с момента повышения.\n" \
               f"Иметь не менее {full_reps} ответов.\n\n" \
               f"🔎 Какие критерии осталось выполнить 🔍\nОтветов: {reps}\n" \
               f"Отстоять дней: {days}\n\nСнять выговоров: {punish[0]}\nСнять предупреждений: {punish[1]}" \
               f"\nСнять устных выговоров: {punish[2]}"

    else:
        return f"✅ Вы выполнили все критерии для получения повышения! Руководство сервера было уведомлено!"


report_message = "Вы хотите отправить уведомление главному администратору о прочтении ваших личных сообщений. Нажмите «Уведомить», чтобы подтвердить действие!"
