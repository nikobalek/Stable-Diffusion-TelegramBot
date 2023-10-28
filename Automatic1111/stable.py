import requests
import io
import base64
from PIL import Image
import threading
import json
import time
from googletrans import Translator

translator = Translator()

sUrl = "http://127.0.0.1:7860"
tApi = "6452554928:AAG3MGE3EYNjFgeticWVGQEHUbqf1cap7dU"
tUrl = "https://api.telegram.org/bot" + tApi

keyboardDefault = [['']]
keyboardStart = [['Generate']]
keyboardModels = [['SD XL', 'Dream ShaperXL'],
                  ['Chillout Mix', 'Realistic Vision']]
keyboardModes = [['Easy Mode', 'Advanced Mode'], ['Costume']]
keyboardSamplers = [['Euler', 'Euler a', 'LMS'], ['Heun', 'DPM2', 'DDIM']]


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
                time.sleep(0.5)
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

        elif text.lower() == "generate":
            sendMessage("Choose Mode", chat_id, keyboardModes)

            mode = Read_input_message(chat_id, offset)
            if mode.lower() == 'easy mode':
                print("easy selected")

                sendMessage("Enter your prompt", chat_id)
                prompt = Read_input_message(chat_id, offset)
                translated = translator.translate(prompt, dest='en')
                prompt = translated.text
                print(prompt)

                sendMessage("Generating Image...", chat_id)
                image = gneratePhoto(prompt)
                sendMessage("Image Generated!", chat_id)

                sendMessage("Uploading Image to Telegram...", chat_id)
                sendPhoto(image, chat_id)

            elif mode.lower() == 'advanced mode':
                print("advaned mode selected")
                sendMessage("Select Model", chat_id, keyboardModels)
                model = Read_input_message(chat_id, offset)
                model = setModel(model)
                print(model)

                refiner = "sd_xl_refiner_1.0_0.9vae.safetensors"

                sendMessage("Select sampler", chat_id, keyboardSamplers)
                sampler = Read_input_message(chat_id, offset)
                print(sampler)

                sendMessage("Enter Steps between 1 and 28", chat_id)
                steps = getSteps(chat_id, offset)
                print(steps)

                sendMessage("Enter CFG between 1 and 7", chat_id)
                cfg = getCfg(chat_id, offset)
                print(cfg)

                sendMessage("Enter your prompt", chat_id)
                prompt = Read_input_message(chat_id, offset)
                prompt = translator.translate(prompt, dest='en')
                print(prompt)

                sendMessage("Generating Image...", chat_id)
                image = gneratePhoto(prompt, steps, cfg,
                                     model, refiner, sampler)
                sendMessage("Image Generated!", chat_id)

                sendMessage("Uploading Image to Telegram...", chat_id)
                sendPhoto(image, chat_id)
            else:
                sendMessage("Under Cunstruction", chat_id, keyboardStart)

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


def getSteps(chat_id, offset):
    steps = Read_input_message(chat_id, offset)
    steps = int(steps)
    while steps > 28 or steps < 0:
        sendMessage("The steps should be between 1 and 28", chat_id)
        steps = Read_input_message(chat_id, offset)
        steps = int(steps)
        if steps > 28 or steps < 0:
            sendMessage("The steps should be between 1 and 28", chat_id)
    return steps


def getCfg(chat_id, offset):
    cfg = Read_input_message(chat_id, offset)
    cfg = int(cfg)
    while cfg > 7 or cfg < 0:
        sendMessage("The CFG should be between 1 and 7", chat_id)
        cfg = Read_input_message(chat_id, offset)
        cfg = int(cfg)
        if cfg > 7 or cfg < 0:
            sendMessage("The CFG should be between 1 and 7", chat_id)
    return cfg


def setModel(model):
    match model:
        case "SD XL":
            model = "sd_xl_base_1.0_0.9vae.safetensors"
        case "Dream ShaperXL":
            model = "dreamshaperXL10_alpha2Xl10.safetensors"
        case "Realistic Vision":
            model = "realisticVisionV51_v51VAE.ckpt"
        case _:
            model = "sd_xl_base_1.0_0.9vae.safetensors"
    return model


def gneratePhoto(prompt,
                 steps=20,
                 cfg=7,
                 checkpiont="sd_xl_base_1.0_0.9vae.safetensors",
                 refiner="sd_xl_refiner_1.0_0.9vae.safetensors",
                 sampler="Euler"
                 ):

    parameters = {
        "prompt": f"{prompt}",
        "steps": f"{steps}",
        "cfg_scale": f"{cfg}",
        "width": 1024,
        "height": 1024,
        "refiner_checkpoint": f"{refiner}",
        "refiner_switch_at": 0.8,
        "hr_checkpoint_name": f"{checkpiont}",
        "sampler_index": f"{sampler}"
    }

    response = requests.post(url=f'{sUrl}/sdapi/v1/txt2img', json=parameters)

    result = response.json()

    imagePath = "C:\\Users\\Arian\\Desktop\\telsends\\photo.JPEG"
    image = Image.open(io.BytesIO(base64.b64decode(result['images'][0])))
    image.save(imagePath, "JPEG", quality=80)

    return imagePath


def sendPhoto(image_path, chat_id):
    with open(image_path, 'rb') as photo:
        response = requests.post(
            tUrl + "/sendPhoto", data={"chat_id": chat_id}, files={"photo": photo})
        print(response)


main()
