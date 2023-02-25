#!/usr/bin/env python3
# -*-coding:utf-8-*-

from chatgpt_wrapper1 import ChatGPT
from text_to_speech import text_to_speech
from speech_to_text import listen_audio
import json
import yaml
import os
import time

# init variable
dir_path = os.path.dirname(os.path.realpath(__file__))

use_speaker = True
input_text = ""
language = "ja"

# creat chatbot of chatGPT
chatbot_GPT = ChatGPT()

# get data dictionary to training
with open(dir_path + '/train/train_dict.json') as json_file:
    data_dict = json.load(json_file)
# get keyword default dictionnary
with open(dir_path + '/train/keywords_default.json') as json_file:
    keywords_dict = json.load(json_file)
# print(keywords_dict)

have_keywords = False
keyword_finded = ""

while True :
    try:
        input_text = input("Mời bạn hỏi: ")
        # input_text = listen_audio(language).lower()
        if input_text == "Keyboard Interrupted":
            break
        if (input_text == 'None'): # or (len(input_text) < 3) :
            print("input text is None")
            time.sleep(0.1)
            continue

        if (u"tạm biệt" in input_text) or (u"goodbye" in input_text) or (u"cảm ơn" in input_text) or (u"ありがとう" in input_text):
            if use_speaker:
                if language == "vi":
                    text_to_speech("Tạm biệt quý khách, hẹn gặp lại quý khách.", language)
                if language == "ja":
                    text_to_speech("さようならお客様、またお会いしましょう。", language)
                if language == "en":
                    text_to_speech("Goodbye and see you again soon.", language)
            break

        # Kiểm tra từ khóa đặc biệt trong câu hỏi hay không
        have_keywords = False
        keyword_finded = ""
        for keyword_str in keywords_dict:
            if keyword_str in input_text:
                have_keywords = True
                # nếu có nhiều keyword cùng xuất hiện thì lấy keyword dài nhất
                if len(keyword_str) > len(keyword_finded):
                    keyword_finded = keyword_str

        # nếu chatbot mkac không trả lời được
        # nếu có keyword thì trả lời theo mặc định của keyword
        if have_keywords:
            response = data_dict[str(keywords_dict[keyword_finded])]
            print("ChatBot:#", response)
            if use_speaker:
                text_to_speech(response)
        else:
            # nếu không có keyword thì hỏi chatGPT
            # loại trừ những câu hỏi quá ngắn có thể do âm thanh nhiễu
            if len(input_text) < 2:
                print("input text is short: ", len(input_text))
                continue
            # hỏi chatgpt với các câu hỏi đủ dài
            print("ChatGPT:>>")
            response = chatbot_GPT.ask(input_text, speak=use_speaker, language=language)
            # print(response)

    except KeyboardInterrupt:
        print ('Keyboard Interrupted1')
        break

    except:
        print("chatbot error!!!")
        if use_speaker:
            if language == "vi":
                text_to_speech("Xin lỗi, tôi đã gặp sự cố khi tìm câu trả lời.", language)
            if language == "ja":
                text_to_speech("申し訳ありませんが、答えを見つけるのに苦労しました。", language)
            if language == "en":
                text_to_speech("Sorry, I had trouble finding the answer.", language)
