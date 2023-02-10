#!/usr/bin/env python3
from chatgpt_wrapper1 import ChatGPT
from text_to_speech import text_to_speech
from speech_to_text import listen_audio

bot = ChatGPT()
input_text = ""
language = "vi"
while True :
    # input_text = input("Mời bạn hỏi: ")

    input_text = listen_audio(language).lower()
    if input_text == 'None' :
        continue
    if ("exit" in input_text):
        break
    response = bot.ask(input_text)
    print(response)  # prints the response from chatGPT

    text_to_speech(response)