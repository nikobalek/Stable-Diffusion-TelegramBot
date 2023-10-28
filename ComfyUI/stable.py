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
filename= ""
comfyUrl = "http://127.0.0.1:8188/prompt"
tApi = "6927275754:AAFFcZ3HEOweLoURZocIg0RI9MornR5_4F8"
tUrl = "https://api.telegram.org/bot" + tApi

outputPath = "C:\\Program Files (x86)\\ComfyUI_windows_portable\\ComfyUI\\output"

keyboardDefault = [['']]
keyboardStart = [['Generate']]
keyboardModes = [['Easy Mode', 'Advanced Mode'], ['Costume']]


def main():
    offset = 0
    while True:
        messages = Read_message(offset)

        if "result" in messages:
            if messages["result"]:
                for message in messages["result"]:
                    threading.Thread(target=process_message,
                                     args=(message, offset)).start()
                offset = messages["result"][-1]["update_id"] + 1
                time.sleep(0.2)
        else:
            continue


def process_message(message, offset):
    try:
        text = message["message"]["text"]
        chat_id = message["message"]["chat"]["id"]
        username = message["message"]["from"]["username"]

        print(username+": "+text)

        if text == "\start" or text == "/start" or text == "start":
            sendMessage("Welcum!💦\nTo Text to Image!📸\nHow to use?🤔\nJust simply send your prompt and I will genarate your image!\nFor more info how to make a better photo tap \\help\nWhen ever stuck somewhere just type start to restart!\n\nMade by @nikobalek", chat_id, keyboardStart)
        elif text.lower() == "hi" or text.lower() == "hello" or text.lower() == "bye":
            sendMessage(
                f"What the FUCK is {text}?!\nGIVE ME PROMPT BITCH!", chat_id, keyboardStart)

        elif text.lower() == "generate" or text.lower() =="/generate" or text.lower() =="gen":
            sendMessage("Enter your prompt", chat_id)
            prompt = Read_input_message(chat_id, offset)
            translated = translator.translate(prompt, dest='en')
            prompt = translated.text
            print(prompt)

            sendMessage("Generating Image...", chat_id)
            if os.path.isdir(f"{outputPath}\\{chat_id}"):
                print("dir exists")
                if os.path.isfile(f'{outputPath}\\{chat_id}\\{chat_id}.txt'):
                    print("file exists")
                    with open(f'{outputPath}\\{chat_id}\\{chat_id}.txt','r') as f:
                        file_number = f.read()
                        print(file_number)
                else:
                    print("file doesnt exist")
                    file_number = 1
            else:
                print("dir doesnt exist")
                file_number = 1
                    
            image = gneratePhoto(prompt, chat_id, file_number)
            time.sleep(15)
            sendMessage("Image Generated!", chat_id)

            sendMessage("Uploading Image to Telegram...", chat_id)
            sendPhoto(image, chat_id)
            sendMessage(f"Your {prompt} is Successfully Made!", chat_id, keyboardStart)
    except:
        sendMessage("Try again please", chat_id, keyboardStart)
        print("An error occurred")


def Read_message(offset):
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
                        Read_message(offset)
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
        with open(f'{outputPath}\\{chat_id}\\{chat_id}.txt','w') as f:
            f.write(file_number)
    else:
        os.mkdir(f'{outputPath}\\{chat_id}')
        with open(f'{outputPath}\\{chat_id}\\{chat_id}.txt','w') as f:
            f.write(file_number)
    
    return imagePath

main()
