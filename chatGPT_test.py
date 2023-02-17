#!/usr/bin/env python3
from chatgpt_wrapper1 import ChatGPT
from text_to_speech import text_to_speech
from speech_to_text import listen_audio
import os

bot = ChatGPT()
input_text = ""
language = "vi"
dir_path = os.path.dirname(os.path.realpath(__file__))
while True :
    input_text = input("Mời bạn hỏi: ")

    # input_text = listen_audio(language).lower()
    if input_text == 'None' :
        continue
    if ("tạm biệt" in input_text) or ("goodbye" in input_text):
        text_to_speech("Tạm biệt quý khách, hẹn gặp lại quý khách.")
        break
    print("ChatGPT:>>>")
    response = bot.ask(input_text)
    # print(response)  # prints the response from chatGPT

    # text_to_speech(response)