import gspread

from cfg import rank_up, SCOPE
from oauth2client.service_account import ServiceAccountCredentials

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").worksheet("Успеваемость администрации")
punish = client.open("ADMINS RED1").worksheet("Логи выговоров")


def get_default_info(array: list) -> str:
    """Функция получения стандартной информации об администраторе"""
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


def get_info_about_rank(array: list) -> str:
    """Функция получения информации о повышении администратора"""
    admin_lvl = array[12]

    rank_standards = {
        "1": {"days": 14, "reports": 5000, "this_rank": "Младшего Модератора", "next_rank": "Модератора"},
        "2": {"days": 21, "reports": 7500, "this_rank": "Модератора", "next_rank": "Старшего Модератора"},
        "2.5": {"days": 30, "reports": 10000, "this_rank": "Старшего Модератора", "next_rank": "Администратора"},
        "3": {"days": 40, "reports": 25000, "this_rank": "Администратора", "next_rank": "Старшего Администратора"}
    }

    if float(admin_lvl) < 4:
        reports = int(array[17])
        up_days = int(array[18])
        punishes = [int(array[14]), int(array[15]), int(array[16])]

        t = f"С {rank_standards[admin_lvl]['this_rank']} на {rank_standards[admin_lvl]['next_rank']}:"

        days_by_lvl = int(rank_standards[admin_lvl]['days'])
        reps_by_lvl = int(rank_standards[admin_lvl]['reports'])

        if days_by_lvl > up_days and reps_by_lvl > reports:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), (days_by_lvl - up_days), punishes, 0, t)

        elif days_by_lvl > up_days and reps_by_lvl <= reports:
            return rank_up(reps_by_lvl, days_by_lvl, 0, (days_by_lvl - up_days), punishes, 0, t)

        elif days_by_lvl <= up_days and reps_by_lvl > reports:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punishes, 0, t)

        else:
            return rank_up(reps_by_lvl, days_by_lvl, (reps_by_lvl - reports), 0, punishes, 1, t)
    else:
        return "Достигнут максимальный админ-уровень!"


def punishment(nick_name: str, is_big=None) -> str:
    array = punish.findall(nick_name, in_column=1)
    rows = list(map(lambda el: el.row, array))

    if len(rows) > 40 and is_big is True:
        rows = rows[-40:]
    else:
        rows = rows[-10:]

    text = ""
    for row in rows:
        st = punish.row_values(row)
        text += f"{st[5]} | {st[2]} {st[3].lower()} | Количество: {st[4]}\nПричина: {st[1]} by {st[6]}\n"

    return text
