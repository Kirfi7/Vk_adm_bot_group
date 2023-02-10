import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("ADMINS RED1").sheet1

data = sheet.get_all_values()

# cola = sheet.col_values(14)
# col = sheet.col_values(2)
# cole = sheet.col_values(15)
# coli = sheet.col_values(16)

rowi = sheet.row_values(3)


pprint(rowi[:16])
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
# numRows = sheet.row_count  # Get the number of rows in the sheet

vk_session = vk_api.VkApi(token="vk1.a.RcpYvhXvj2P9NOfFXQ_ycHiFm1ENdqSKt4iRTR4_YltoNejArEwUNnQqy--Hq3vvyG_3-smfpgjNT-rHuUpNVcdJfMBRvV7CXhw0eL-T6dBYW-nAI1t_9834yfJpQBQaO1Y2Is9lRjDePfVEGwObaCyNOEWXaZL_K4OC9a7XXgbrpgGm-6vMOxShAufDs46qU34iqIervEGqItexmEX8nA")
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id":id, "message":some_text,"random_id":0})

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            rowi = sheet.row_values(3)
            ala = list(rowi[:16])
            kek = ' '.join(ala)
            if msg == "hihihi":
                send_some_msg(id, f'{kek}')
                # апе