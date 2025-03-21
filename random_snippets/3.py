import requests
from urllib3.exceptions import InsecureRequestWarning
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from urllib3.exceptions import InsecureRequestWarning

IP = '0.0.0.0'
TOKEN = 'somerandomtoken'
CHATID = -1000000001
APPLICATION = 'someapplication'

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

def send_to_telegram(message):
    try:
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={'chat_id': CHATID, 'text': message})
    except Exception as e:
        print(e)

def start():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    url = f"https://{IP}:8443/DiaManT/api/internal/dialogs/?compact=True"
    payload = json.dumps({
    "application_id": APPLICATION,
    "source": "chat",
    "user": {
        "user_id": "string",
        "username": "string"
    },
    "context": {
        "semantics": {
        "channel": "chat",
        "chatBotChannel": "telegram"
        },
        "asr_info": {}
    }
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload,verify=False) 
    if response.status_code == 403:
        return 'ERROR', 'ERROR'
    else:
        dialog_id = response.json().get('dialogId')
        x1 = response.json().get("prompt").replace('|', '')

        return x1, dialog_id

def naxabare(txtUser, dialog_id):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    url = f"https://{IP}:8443/DiaManT/api/internal/dialogs/"+dialog_id+'?compact=True'
    payload = json.dumps({
    "application_id": APPLICATION,
    "utterance": txtUser
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    if response.status_code == 404:
        return 'ERROR'
    else:
        x2 = response.json().get("prompt").replace('|', '')
        return x2

@dp.message_handler(commands = 'start')
async def new_message(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username

    with open('dialogs.txt', 'r') as file:
        content = file.read()

    lines = content.split('\n')
    filtered_lines = [line for line in lines if len(line.split(',')) > 1 and line.split(',')[1] != str(chat_id)]

    new_content = '\n'.join(filtered_lines)
    with open('dialogs.txt', 'w') as file:
        file.write(new_content)

    xxx, dialogID = start()
    if xxx == 'ERROR':

        await message.answer('нажми на /start чтобы начать')
    else:
        new_line_to_add = f"\n{dialogID},{chat_id}"
        with open('dialogs.txt', 'a') as file:
            print(new_line_to_add, file=file)
        send_to_telegram('Пользователь @' + str(username) + ' начал новый диалог\n' + dialogID + '\nchatID: ' + str(chat_id))
        await message.answer(xxx)

@dp.message_handler(content_types = ["text"])
async def step1(message: types.Message):
    if message.text.startswith(""):
        flag, flag2 = False, False
        chat_id = message.chat.id 

        with open('dialogs.txt', 'r') as file:
            content = file.read()
        x = content.split('\n')
        filtered_list = list(filter(None, x))

        for i in range(len(filtered_list)):
            tempCHATID = filtered_list[i].split(',')[1]
            if str(chat_id) == tempCHATID:
                flag = True
                tempDialogID = filtered_list[i].split(',')[0]
                
                responseX = naxabare(message.text, tempDialogID)
                send_to_telegram(tempDialogID +'\n' + '\nТекст: ' + message.text + '\nОтвет: ' + responseX)
                await message.answer(responseX)

                if responseX == 'ERROR':
                    await message.answer('нажми на /start чтобы начать')
                break 
        if flag==False:
            await message.answer('нажми на /start чтобы начать')

executor.start_polling(dp, skip_updates = True)
