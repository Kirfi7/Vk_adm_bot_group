from cfg import rank_up


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
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), (days_by_lvl - up_date), punish, 0, t)
        elif days_by_lvl > up_date and reps_by_lvl <= reports:
            return rank_up(reps_by_lvl, days_by_lvl, 0, (days_by_lvl - up_date), punish, 0, t)
        elif days_by_lvl <= up_date and reps_by_lvl > reports:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punish, 0, t)
        else:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punish, 1, t)
    else:
        return "Достигнут максимальный админ-уровень!"


def get_rank_standard(array):
    post = array[2]
    second = array[3]
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
        "К": "Ответы: 50 штук\nОнлайн: 150 минут",
        "ЗГА": "Ответы: 1000 штук\nОнлайн: 1440 минут",
        "ГА": "Ответы: 30 штук\nОнлайн: 90 минут"
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
    elif "Куратор" in post:
        standard = str(rank_standards['К'])
    elif "Главный Администратор" in post:
        standard = str(rank_standards['ГА'])
    elif "Заместитель Главного Администратора" in post:
        standard = str(rank_standards['ЗГА'])
    else:
        standard = "Ошибка. Сообщите об это сюда:\n@kirfibely или @xm_pearson"
    return f"📆 Ваш норматив 📆\n{standard}"