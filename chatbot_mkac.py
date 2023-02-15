#!/usr/bin/env python3
# -*-coding:utf-8-*-

from chatgpt_wrapper1 import ChatGPT
from text_to_speech import text_to_speech
from speech_to_text import listen_audio
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
import yaml
import os
import time

# init variable
dir_path = os.path.dirname(os.path.realpath(__file__))

input_text = ""
language = "vi"

# remove old file training
os.remove(dir_path + "/db.sqlite3")
time.sleep(1.0)

# creat chatbot of chatGPT
chatbot_GPT = ChatGPT()

# creat chatbot of MKAC
chatbot_MKAC = ChatBot(
    "My ChatterBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    # database_uri="sqlite:///db.sqlite3",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I do not understand',
            'maximum_similarity_threshold': 0.95
        }
    ]
)
# get data dictionary to training
with open(dir_path + '/train/train_dict.json') as json_file:
    data_dict = json.load(json_file)
# get keyword default dictionnary
with open(dir_path + '/train/keywords_default.json') as json_file:
    keywords_dict = json.load(json_file)
print(keywords_dict)


# training for chatbot mkac
trainer = ChatterBotCorpusTrainer(chatbot_MKAC)
trainer.train(dir_path + '/train/train_data.json')
# trainer.train('chatterbot.corpus.english.greetings')

have_keywords = False
keyword_finded = ""

while True :
    try:
        input_text = input("Mời bạn hỏi: ")
        # input_text = listen_audio(language).lower()
        if input_text == 'None' :
            continue
        if ("tạm biệt" in input_text) or ("goodbye" in input_text):
            text_to_speech("Tạm biệt quý khách, hẹn gặp lại quý khách.")
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

        # use chatbot MKAC first

        response = str(chatbot_MKAC.get_response(input_text))
        if response != 'I do not understand':
            # nếu chatbot mkac trả lời được
            # print("ChatBot:$", response)
            if str(response) in data_dict:
                # print("co trong tu dien")
                response = data_dict[str(response)]
            print("ChatBot:$", response)
            text_to_speech(response)
        else:
            # nếu chatbot mkac không trả lời được
            # nếu có keyword thì trả lời theo mặc định của keyword
            if have_keywords:
                response = data_dict[str(keywords_dict[keyword_finded])]
                print("ChatBot:#", response)
                text_to_speech(response)
            else:
                # nếu không có keyword thì hỏi chatGPT
                # loại trừ những câu hỏi quá ngắn có thể do âm thanh nhiễu
                if len(input_text) < 10:
                    continue
                # hỏi chatgpt với các câu hỏi đủ dài
                print("ChatGPT:>>")
                response = chatbot_GPT.ask(input_text)
                # print(response)

    except:
        print("chatbot error!!!")
        text_to_speech("Xin lỗi, tôi đã gặp sự cố khi tìm câu trả lời.")
