import requests
import io
import base64
from PIL import Image
import threading
import json


sUrl = "http://127.0.0.1:7860"
tApi = "6452554928:AAG3MGE3EYNjFgeticWVGQEHUbqf1cap7dU"
tUrl = "https://api.telegram.org/bot" + tApi

keyboardDefault =[['']]
keyboardStart = [['Generate']]
keyboardModel = [['SD XL','Dream ShaperXL'],['Chillout Mix', 'Real Vision']]
keyboardModes = [['Easy Mode','Advanced Mode']]


def main():
    offset = 0
    while True:
        messages = Read_message(offset)
    
        #check if there is any message
        if messages["result"]:
        
            #for every message make a thread
            for message in messages["result"]:
                threading.Thread(target=process_message, args=(message, offset)).start()
                
            #next message
            offset = messages["result"][-1]["update_id"] + 1
            
            
def process_message(message, offset):
                try:
                    text =     message["message"]["text"]
                    chat_id =  message["message"]["chat"]["id"]
                    username = message["message"]["from"]["username"]
                
                    print(username+": "+text)
                    
                    if text == "\start" or text == "/start" or text == "start":
                        sendMessage("Welcum!💦\nTo Text to Image!📸\nHow to use?🤔\nJust simply send your prompt and I will genarate your image!\n\nMade by @nikobalek", chat_id, keyboardStart)
                    elif text.lower() == "hi" or text.lower() == "hello" or text.lower() == "bye":
                        sendMessage(f"What the FUCK is {text}?!\nGIVE ME PROMPT BITCH!", chat_id, keyboardStart)
                    elif text.lower() == "generate":
                        sendMessage("simply send your prompt for text to image",chat_id)
                    else:
                        sendMessage("Enter your prompt", chat_id)
                        
                        sendMessage("Generating Image...", chat_id)
                        image = gneratePhoto(text)
                        sendMessage("Image Generated!", chat_id)
                        
                        sendMessage("Uploading Image to Telegram...", chat_id)
                        sendPhoto(image, chat_id)
                        
                except:
                    sendMessage("Try again please", chat_id)
                    print("An error occurred")
            
            
def Read_message (offset):
    parameters = {
        "offset": offset,
        "limit": 1
    }
    response = requests.get(tUrl + "/getUpdates", data = parameters)
    data = response.json()
    return data


def Read_input_message(chat_id, offset):
    while True:
        messages = Read_message(offset)
        
        if messages["result"]:
            for message in messages["result"]:
                if chat_id == message["message"]["chat"]["id"]:
                    input = message["message"]["text"]
                    offset = messages["result"][-1]["update_id"] + 1
                    Read_message(offset)
                    return input
            offset = messages["update_id"] + 1

    
def sendMessage(text, id, keyboard = keyboardDefault):
    headers = {'Content-type': 'application/json'}
    parameters = {
        'chat_id': id,
        'text': text,
        'reply_markup': {
            'keyboard':keyboard,
            'resize_keyboard':True,
            'one_time_keyboard':True
        }
    }
    response = requests.get(tUrl + "/sendMessage", data = json.dumps(parameters), headers = headers)


def gneratePhoto(prompt):
    
    parameters = {
    "prompt": f"{prompt}",
    "steps": 28,
    "cfg_scale": 8.5,
    "width": 1024,
    "height": 1024,
    "refiner_checkpoint": "sd_xl_refiner_1.0_0.9vae.safetensors",
    "refiner_switch_at": 0.8,
    "hr_checkpoint_name": "dreamshaperXL10_alpha2Xl10.safetensors",
    "sampler_index": "Euler a"
    }

    response = requests.post(url=f'{sUrl}/sdapi/v1/txt2img', json=parameters)

    result = response.json()
    print(result)
    
    imagePath = "C:\\Users\\Arian\\Desktop\\telsends\\photo.JPEG"
    image = Image.open(io.BytesIO(base64.b64decode(result['images'][0])))
    image.save(imagePath,"JPEG", quality = 80)
     
    return imagePath
    

def sendPhoto(image_path ,chat_id):
     with open(image_path, 'rb') as photo:
        response = requests.post(tUrl + "/sendPhoto", data = {"chat_id": chat_id}, files={"photo": photo})
        print(response)
        
    
main()