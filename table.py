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
        "1": {"days": 14, "reports": 5000, "this_rank": "Младшего Модератора", "next_rank": "Модератора"},
        "2": {"days": 25, "reports": 1000, "this_rank": "Модератора", "next_rank": "Администратора"},
        "3": {"days": 50, "reports": 25000, "this_rank": "Администратора", "next_rank": "Старшего Администратора"}
    }

    if int(admin_lvl) < 4:
        reports = int(array[17]); up_days = int(array[18])
        punish = [int(array[14]), int(array[15]), int(array[16])]

        t = f"С {rank_standards[admin_lvl]['this_rank']} на {rank_standards[admin_lvl]['next_rank']}:"

        days_by_lvl = int(rank_standards[admin_lvl]['days'])
        reps_by_lvl = int(rank_standards[admin_lvl]['reports'])

        if days_by_lvl > up_days and reps_by_lvl > reports:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), (days_by_lvl - up_days), punish, 0, t)

        elif days_by_lvl > up_days and reps_by_lvl <= reports:
            return rank_up(reps_by_lvl, days_by_lvl, 0, (days_by_lvl - up_days), punish, 0, t)

        elif days_by_lvl <= up_days and reps_by_lvl > reports:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punish, 0, t)

        else:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punish, 1, t)
    else:
        return "Достигнут максимальный админ-уровень!"


def get_rank_standard(array):
    post = array[2]
    second = array[3]
    level = f"{array[12]}lvl"

    rank_standards = {
        "1lvl": "Ответы: 250 штук\nОнлайн: 150 минут\nНаказаний: 10 штук",
        "2lvl": "Ответы: 200 штук\nОнлайн: 150 минут\nНаказаний: 10 штук\nМероприятия: 2 штуки",
        "МК": "Ответы: 175 штук\nОнлайн: 150 минут\nНаказаний: 15 штук\nПост: За своей фракцией",
        "МФ": "Ответы: 150 штук\nОнлайн: 120 минут\nНаказаний: 10 штук\nФорум: 10 ответов\nМероприятия: 1 штука",
        "ФК": "Ответы: 170 штук\nОнлайн: 150 минут\nНаказаний: 15 штук\nПост: За своей фракцией\nФорум: 10 ответов\nМероприятия: 1 штука",
        "3lvl": "Ответы: 200 штук\nОнлайн: 150 минут\nНаказаний: 15 штук\nМероприятия: 2 штуки",
        "4lvl": "Ответы: 200 штук\nОнлайн: 150 минут\nНаказаний: 20 штук\nМероприятия: 1 штука",
        "ЗГС": "Ответы: 120 штук\nОнлайн: 130 минут\nНаказаний: 10 штук",
        "ГС": "Ответы: 100 штук\nОнлайн: 150 минут\nНаказаний: 5 штук",
        "К": "Ответы: 50 штук\nОнлайн: 150 минут",
        "ЗГА": "Ответы: 1000 штук\nОнлайн: 1440 минут",
        "ГА": "Ответы: 30 штук\nОнлайн: 90 минут"
    }

    points_standards = {
        "1lvl": "Ответы: 250 штук\nОнлайн: 180 минут\nВыплата: 50 epoints",
        "2lvl": "Ответы: 200 штук\nОнлайн: 180 минут\nВыплата: 55 epoints",
        "3lvl": "Ответы: 180 штук\nОнлайн: 180 минут\nВыплата: 70 epoints",
        "4lvl": "Ответы: 125 штук\nОнлайн: 150 минут\nВыплата: 90 epoints",
        "ГА": "Ответы: 30 штук\nОнлайн: 90 минут\nВыплата: 100 epoints",
        "ГС": "Ответы: 75 штук\nОнлайн: 150 минут\nВыплата: 85 epoints",
        "ГС_Х": "Ответы: 75 штук\nОнлайн: 150 минут\nВыплата: 90 epoints",
        "ЗГС": "Ответы: 100 штук\nОнлайн: 150 минут\nВыплата: 80 epoints",
        "ЗГА": "Ответы: 25 штук\nОнлайн: 120 минут\nВыплата: 95 epoints",
        "К": "Ответы: 50 штук\nОнлайн: 150 минут\nВыплата: 90 epoints"
    }

    if "Младший Модератор" in post:
        standard = rank_standards["1lvl"]
        points = points_standards["1lvl"]

    elif "Модератор" in post:
        if "МК" in second and "МФ" in second:
            standard = rank_standards["ФК"]
            points = points_standards["2lvl"]
        elif "МК" in second:
            standard = rank_standards["МК"]
            points = points_standards["2lvl"]
        elif "МФ" in second:
            standard = rank_standards["МФ"]
            points = points_standards["2lvl"]
        else:
            standard = rank_standards["2lvl"]
            points = points_standards["2lvl"]

    elif "Администратор" in post:
        if "МК" in second and "МФ" in second:
            standard = rank_standards["ФК"]
            points = points_standards["3lvl"]
        elif "МК" in second:
            standard = rank_standards["МК"]
            points = points_standards["3lvl"]
        elif "МФ" in second:
            standard = rank_standards["МФ"]
            points = points_standards["3lvl"]
        else:
            standard = rank_standards["3lvl"]
            points = points_standards["3lvl"]

    elif "Старший Администратор" in post:
        if "МК" in second and "МФ" in second:
            standard = rank_standards["ФК"]
            points = points_standards["4lvl"]
        elif "МК" in second:
            standard = rank_standards["МК"]
            points = points_standards["4lvl"]
        elif "МФ" in second:
            standard = rank_standards["МФ"]
            points = points_standards["4lvl"]
        else:
            standard = rank_standards["4lvl"]
            points = points_standards["4lvl"]

    elif "Заместитель Главного Следящего" in post:
        if "ГОСС" in post or "ОПГ" in post or "Хелперами" in post:
            standard = rank_standards["ЗГС"]
            points = points_standards["ЗГС"]
        else:
            standard = rank_standards["ЗГС"]
            points = points_standards[level]

    elif "Главный Следящий" in post:
        if "Хелперами" in post:
            standard = rank_standards["ГС"]
            points = points_standards["ГС_Х"]
        elif "ГОСС" in post or "ОПГ" in post:
            standard = rank_standards["ГС"]
            points = points_standards["ГС"]
        else:
            standard = rank_standards["ГС"]
            points = points_standards[level]

    elif "Куратор Администрации" in post:
        standard = rank_standards["К"]
        points = points_standards["К"]

    elif "Заместитель Главного Администратора" in post:
        standard = rank_standards["ЗГА"]
        points = points_standards["ЗГА"]

    elif "Главный Администратор" in post:
        standard = rank_standards["ГА"]
        points = points_standards["ГА"]

    else:
        return "Ошибка! Сообщите это @xm_pearson или @kirfibely"

    return f"📆 Ваш норматив 📆\n{standard}\n\n💰 Норматив epoints 💰\n{points}"


def ranked_up(array):
    admin_lvl = array[12]

    rank_standards = {
        "1": {"days": 14, "reports": 5000},
        "2": {"days": 25, "reports": 10000},
        "3": {"days": 50, "reports": 25000}
    }

    if int(admin_lvl) < 4:
        reports = int(array[17]); up_days = int(array[18])
        punish = 1 if (int(array[14]) + int(array[15]) + int(array[16])) == 0 else 0

        days_by_lvl = int(rank_standards[admin_lvl]['days'])
        reps_by_lvl = int(rank_standards[admin_lvl]['reports'])

        if punish == 1 and reports >= reps_by_lvl and up_days >= days_by_lvl:
            return 1, [admin_lvl, array[1]]

    return 0, 0
