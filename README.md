# Stable Diffusion Telegram Bot
#### Video Demo: [Video Demo URL](<https://youtu.be/zBZyMhIeArk>)
#### Description:

## Introduction

Welcome to the Text-to-Image Telegram Bot project! This bot allows users to generate images from textual descriptions directly through Telegram. It leverages a local image generation service and responds to user commands in a conversational manner. Whether you want to create art, visualize concepts, or just have some fun with AI-generated images, this bot is here to help.

## Project Overview

This project is implemented in Python and uses several libraries and APIs to function effectively. The main script, `stable.py`, handles all interactions with the Telegram API and the local image generation service. It includes features for starting and guiding users, generating images from text prompts, and managing ongoing operations.

## Features

- **Start and Help Commands**: Provides guidance to users on how to interact with the bot.
- **Image Generation**: Converts text prompts into images using a local image generation service.
- **Cancel Operations**: Allows users to cancel ongoing prompts or image generation processes.
- **Support Messages**: Users can send messages to the bot admin for support.
- **Archive Access**: Users can view previously generated images.

## File Overview

### `stable.py`

This is the main script of the project. Below is an overview of its primary components:

- **Libraries and Initialization**: The script imports necessary libraries such as `requests`, `googletrans`, and `Pillow`. It also initializes variables like the Telegram Bot API token and the URL for the local image generation service.

- **Main Function**: 
  - `main()`: This function continuously polls the Telegram API for new messages and handles them using the `process_message` function.

- **Message Processing**:
  - `process_message(message, offset)`: This function processes incoming messages, determines the type of command or text received, and executes appropriate actions. It supports commands like `/start`, `/help`, and prompts like "Imagine!".

- **Helper Functions**:
  - `getMessage(offset)`: Retrieves messages from the Telegram API.
  - `sendMessage(text, id, keyboard=keyboardDefault)`: Sends messages to users.
  - `sendPhoto(image_path, chat_id)`: Sends generated images to users.
  - `gneratePhoto(userprompt, chat_id, file_number)`: Generates images from text prompts using the local image generation service.
  - `isGenerating(chat_id)`, `isPrompting(chat_id)`: Check the status of various operations.
  - `waitForPhotoToGenerate(photoPath, userWhoRequested)`: Waits for image generation to complete and informs the user.

### Design Choices

1. **Local Image Generation Service**: The bot uses a local service for generating images from text prompts. This decision was made to ensure quick response times and to avoid dependency on third-party services.

2. **Google Translate Integration**: To handle prompts in different languages, the `googletrans` library is used for translating non-English text to English. This ensures the image generation service receives consistent input.

3. **Asynchronous Processing**: The bot uses threading to handle multiple user requests simultaneously. This improves user experience by allowing the bot to process new messages while generating images.

4. **User Guidance**: The bot provides a conversational interface with clear instructions and feedback messages. This helps users understand how to interact with the bot and utilize its features effectively.

## How to Use

1. **Setup**:
   - Clone the repository or download the `stable.py` script.
   - Install the required Python libraries using:
     ```bash
     pip install requests googletrans Pillow
     ```
   - Ensure your local image generation service is running and accessible at `http://127.0.0.1:8188`.

2. **Configuration**:
   - Replace the placeholder `tApi` in the script with your Telegram Bot API token.

3. **Run the Bot**:
   - Start the bot by running the script:
     ```bash
     python stable.py
     ```

4. **Interact with the Bot**:
   - Send `/start` to initiate the bot and get a welcome message.
   - Use the provided buttons to send text prompts and generate images.
   - View archived images or contact the bot admin for support if needed.

## Conclusion

This Text-to-Image Telegram Bot provides an intuitive and interactive way to generate images from text. By leveraging AI and local processing, it ensures quick and effective responses. The project is designed to be user-friendly, with clear guidance and support features. 

We hope you enjoy using the bot and exploring the creative possibilities it offers!
