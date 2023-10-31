import json
from urllib import request, parse
import random
import requests
import threading
import time
import os
from googletrans import Translator
from PIL import Image

translator = Translator()
filename = ""
comfyUrl = "http://127.0.0.1:8188/prompt"
tApi = "6927275754:AAFFcZ3HEOweLoURZocIg0RI9MornR5_4F8"
tUrl = "https://api.telegram.org/bot" + tApi

outputPath = "C:\\Program Files (x86)\\ComfyUI_windows_portable\\ComfyUI\\output"

keyboardDefault = [['']]
keyboardStart = [['Imagine!']]
keyboardCancel = [['Cancel']]
keyboardModes = [['Easy Mode', 'Advanced Mode'], ['Costume']]


def main():
    offset = 0
    try:
        while True:

            messages = getMessage(offset)

            if "result" in messages:
                if messages["result"]:
                    for message in messages["result"]:
                        threading.Thread(target=process_message,
                                         args=(message, offset)).start()
                    offset = messages["result"][-1]["update_id"] + 1
                    time.sleep(0.2)
            pass
    except Exception as e:
        main()
        print(f"something wnent wrong{e}")



def process_message(message, offset):
    try:
        chat_id = message["message"]["chat"]["id"]
        username = message["message"]["from"]["username"]
        if 'text' in message['message']:
            text = message['message']['text']
        else:
            sendMessage("What The Hell Is This?!\nSEND ME TEXT!",chat_id)
            return 0


        print(username+": "+text)

        if text == "\start" or text == "/start" or text == "start":
            sendMessage("welcome!\nTo Text to Image!📸\nHow to use?🤔\nJust simply send your text and I will imagine your text!\nFor more info how to make a better photo tap /help\nWhen ever stuck somewhere just type start to restart!\n\nMade by @nikobalek", chat_id, keyboardStart)
        elif text.lower() == "hi" or text.lower() == "hello" or text.lower() == "bye":
            sendMessage(
                f"What the FUCK is {text}?!\nGIVE ME PROMPT BITCH!", chat_id, keyboardStart)

        elif text.lower() == "imagine!" or text.lower() == "/generate" or text.lower() == "gen":

            if os.path.exists(f"{outputPath}\\{chat_id}"):
                if os.path.exists(f"{outputPath}\\{chat_id}\\isGenerating.txt"):  
                    status = isGenerating(chat_id)
                else:
                    status = '0'
            else:
                status = '0'

            if status == '1':
                sendMessage(
                    "You can only Imagine 1 Text at a time!⚠️", chat_id)
                return 0

            sendMessage("Enter your Text for me to Imagine!",
                        chat_id, keyboardCancel)

            if os.path.exists(f"{outputPath}\\{chat_id}"):
                with open(f"{outputPath}\\{chat_id}\\isPrompting.txt", 'w') as f:
                    f.write("1")
            else:
                os.mkdir(f"{outputPath}\\{chat_id}")
                with open(f"{outputPath}\\{chat_id}\\isPrompting.txt", 'w') as f:
                    f.write("1")

            prompt = Read_input_message(chat_id, offset)

            with open(f"{outputPath}\\{chat_id}\\isPrompting.txt", 'w') as f:
                f.write("0")

            if os.path.exists(f"{outputPath}\\{chat_id}"):
                with open(f"{outputPath}\\{chat_id}\\isGenerating.txt", 'w') as f:
                    f.write("1")
            else:
                os.mkdir(f"{outputPath}\\{chat_id}")
                with open(f"{outputPath}\\{chat_id}\\isGenerating.txt", 'w') as f:
                    f.write("1")

            if prompt.lower() == "imagine!" or prompt.lower() == "/generate" or prompt.lower() == "gen" or prompt.lower() == "\start" or prompt.lower() == "/start" or prompt.lower() == "start" or prompt.lower() == "\help" or prompt.lower() == "/help":
                with open(f"{outputPath}\\{chat_id}\\isPrompting.txt", 'w') as f:
                    f.write("0")
                with open(f"{outputPath}\\{chat_id}\\isGenerating.txt", 'w') as f:
                    f.write("0")
                return 0
            elif prompt.lower() == "cancel":
                with open(f"{outputPath}\\{chat_id}\\isPrompting.txt", 'w') as f:
                    f.write("0")
                with open(f"{outputPath}\\{chat_id}\\isGenerating.txt", 'w') as f:
                    f.write("0")
                sendMessage("Canceled!", chat_id, keyboardStart)
                return 0

            translated = translator.translate(prompt, dest='en')
            prompt = translated.text
            print(prompt)

            sendMessage("Generating Image...", chat_id, keyboardDefault)
            
            file_number = getPhotoNumber(chat_id)
            image = gneratePhoto(prompt, chat_id, file_number)
            waitForPhotoToGenerate(image, chat_id)
            
            with open(f"{outputPath}\\{chat_id}\\isGenerating.txt", 'w') as f:
                f.write("0")
            sendMessage("Uploading Image to Telegram...", chat_id)
            sendPhoto(image, chat_id)
            sendMessage(f"Your {prompt} is Successfully Made!",
                        chat_id, keyboardStart)
            return 0
        elif text.lower() == "support":
            sendMessage("send your message to admin!",chat_id, keyboardCancel)
            uInput = Read_input_message(chat_id, offset)
            if uInput.lower() == "cancel":
                sendMessage("Canceled!", chat_id, keyboardStart)
                return 0
            sendMessage(f"Message from user:\n@{username}: {uInput}",'210895698')
            sendMessage('Message Sent!',chat_id, keyboardStart)
            
        else:
            statusGen = isGenerating(chat_id)
            statusProm = isPrompting(chat_id)

            if statusGen == '0' and statusProm == '1':
                return 0
            elif statusGen == '0' and statusProm == '0':
                sendMessage(
                    'To Imagine a Photo First Tap "Imagine!" Button👇', chat_id, keyboardStart)
                return 0

    except:
        sendMessage("Try again please", chat_id, keyboardStart)
        print("An error occurred")


def getMessage(offset):
    parameters = {
        "offset": offset,
        "limit": 1
    }
    response = requests.get(tUrl + "/getUpdates", data=parameters)
    data = response.json()
    return data


def getMessages():
    response = requests.get(tUrl + "/getUpdates")
    data = response.json()
    return data


def Read_input_message(chat_id, offset):
    while True:
        messages = getMessages()
        if "result" in messages:
            if messages["result"]:
                for message in messages["result"]:
                    if chat_id == message["message"]["chat"]["id"]:
                        input = message["message"]["text"]
                        getMessage(offset)
                        return input
        else:
            continue


def sendMessage(text, id, keyboard=keyboardDefault):
    headers = {'Content-type': 'application/json'}
    parameters = {
        'chat_id': id,
        'text': text,
        'reply_markup': {
            'keyboard': keyboard,
            'resize_keyboard': True,
            'one_time_keyboard': True
        }
    }
    response = requests.get(tUrl + "/sendMessage",
                            data=json.dumps(parameters), headers=headers)


def sendPhoto(image_path, chat_id):
    image = Image.open(f'{image_path}')
    print("image opened")
    image.save(f'{outputPath}\\{filename}.jpg', 'JPEG', quality=80)
    print("image saved")
    imagePath = f'{outputPath}\\{filename}.jpg'

    with open(imagePath, 'rb') as photo:
        response = requests.post(
            tUrl + "/sendPhoto", data={"chat_id": chat_id}, files={"photo": photo})
        print(response)


def gneratePhoto(userprompt, chat_id, file_number):

    seed = random.randint(0, 1000000)
    prompt = userprompt
    times = 0
    fileprefix = chat_id

    data = {
        "3": {
            "inputs": {
                "seed": f"{seed}",
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": [
                    "4",
                    0
                ],
                "positive": [
                    "6",
                    0
                ],
                "negative": [
                    "7",
                    0
                ],
                "latent_image": [
                    "5",
                    0
                ]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0_0.9vae.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": 1024,
                "height": 1024,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": f"{prompt}",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": [
                    "3",
                    0
                ],
                "vae": [
                    "4",
                    2
                ]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": f"{fileprefix}",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImage"
        },
        "11": {
            "inputs": {
                "filename_prefix": f"{chat_id}",
                "filename_keys": "",
                "foldername_prefix": f"{chat_id}",
                "foldername_keys": "",
                "delimiter": "dot",
                "save_job_data": "disabled",
                "job_data_per_image": "disabled",
                "job_custom_text": "",
                "save_metadata": "disabled",
                "counter_digits": 2,
                "counter_position": "last",
                "image_preview": "enabled",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImageExtended"
        }

    }

    print("generating")

    response = requests.post(
        'http://127.0.0.1:8188/prompt', json={'prompt': data})
    result = response.json()

    print(response)
    print(result)

    print("file name def")
    filename = "{}.{:02d}.png".format(chat_id, int(file_number))
    print("image path de")
    imagePath = f"{outputPath}\\{chat_id}\\{filename}"

    print("adding numbers")
    file_number = int(file_number)
    file_number = file_number + 1
    file_number = str(file_number)
    print(file_number)

    print("writing number")
    if os.path.isdir(f'{outputPath}\\{chat_id}'):
        with open(f'{outputPath}\\{chat_id}\\{chat_id}.txt', 'w') as f:
            f.write(file_number)
    else:
        os.mkdir(f'{outputPath}\\{chat_id}')
        with open(f'{outputPath}\\{chat_id}\\{chat_id}.txt', 'w') as f:
            f.write(file_number)

    return imagePath


def getPhotoNumber(chat_id):
    if os.path.isdir(f"{outputPath}\\{chat_id}"):
                if os.path.isfile(f'{outputPath}\\{chat_id}\\{chat_id}.txt'):
                    with open(f'{outputPath}\\{chat_id}\\{chat_id}.txt', 'r') as f:
                        photoNumber = f.read()
                        return photoNumber
                        print(number)
                else:
                    return '1'
    else:
        return '1'


def waitForPhotoToGenerate(photoPath, userWhoRequested):
    #must add a timeout
    while True:
        if os.path.exists(photoPath):
            sendMessage("Image Generated!", userWhoRequested)
            break


def isGenerating(chat_id):
    if os.path.exists(f"{outputPath}\\{chat_id}"):
        if os.path.exists(f"{outputPath}\\{chat_id}\\isGenerating.txt"):
            with open(f"{outputPath}\\{chat_id}\\isGenerating.txt", 'r') as f:
                status = f.read()
                return status
        else:
            return '0'
    else:
        return '0'


def isPrompting(chat_id):
    if os.path.exists(f"{outputPath}\\{chat_id}"):
        if os.path.exists(f"{outputPath}\\{chat_id}\\isPrompting.txt"):
            with open(f"{outputPath}\\{chat_id}\\isPrompting.txt", 'r') as f:
                status = f.read()
                return status
        else:
            return '0'
    else:
        return '0'


def isSendingMessage(chat_id):
    if os.path.exists(f"{outputPath}\\{chat_id}"):
        if os.path.exists(f"{outputPath}\\{chat_id}\\isSendingMessage.txt"):
            with open(f"{outputPath}\\{chat_id}\\isSendingMessage.txt", 'r') as f:
                status = f.read()
                return status
        else:
            return '0'
    else:
        return '0'


main()