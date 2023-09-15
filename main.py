import threading
import notify

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from table import get_default_info, get_info_about_rank, punishment
from functions import *

lp = VkBotLongPoll(vk=vk_session, group_id=209878062)


def callback_handler(event):
    data = event.object.payload
    user_id = event.object["user_id"]

    if data["type"] == "send":
        notify.send_notify(user_id, get_name(user_id))
        editor(user_id, event.object.conversation_message_id,
               "Уведомление успешно отправлено!")

    elif data["type"] == "deny":
        editor(user_id, event.object.conversation_message_id,
               "Отправка уведомления отменена!")


def message_handler(event):
    text = event.message.text
    user_id = event.message["from_id"]
    is_access = access(user_id)

    if is_access[1] != 1:
        return

    nick_name = sheet.cell(is_access[0], 2).value

    if text == "Начать":
        get_keyboard(user_id)

    if text == "Основная информация":
        member_array = get_array(user_id)
        sender(user_id, get_default_info(member_array))

    if text == "Последние наказания":
        sender(user_id, "Последние 10 действий с наказаниями:\n\n" + punishment(nick_name))

    if text == "Инфа о повышении":
        member_array = get_array(user_id)
        sender(user_id, get_info_about_rank(member_array))

    if text == "Связаться с ГА":
        send_report_message(user_id, event.message.id)

    cmd = text[1:]
    if text[0] in ["/", "!", "+"] and cmd.split()[0] in config.CMDS:

        if cmd == "update" and user_id in config.ACCESS:
            all_admins = list(set(sheet.col_values(7)))[2:]
            [get_keyboard(admin) for admin in all_admins]
            return

        array = cmd.split()
        if len(array) == 0:
            sender(user_id, "Введите команду повторно, указав никнейм админа.")
            return

        if "punish" in cmd:
            argument = array[1]
            sender(user_id, punishment(argument, is_big=True))


def event_handler(event):
    print(event)
    try:
        if event.type == VkBotEventType.MESSAGE_NEW and not event.from_chat:
            message_handler(event)

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            callback_handler(event)

    except:
        raise


def main():
    while True:
        try:
            for event in lp.listen():
                threading.Thread(target=event_handler, args=(event,)).start()

        except:
            raise


if __name__ == "__main__":
    main()
