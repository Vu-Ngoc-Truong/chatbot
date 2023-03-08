#!/usr/bin/env python3
# -*-coding:utf-8-*-

from chatgpt_wrapper1 import ChatGPT
from text_to_speech import text_to_speech
from speech_to_text import listen_audio
import json
import yaml
import os
import time


class Chatbot:
    def __init__(self, language='vi', use_speaker=True):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.language = language
        self.use_speaker = use_speaker
        self.chatbot_GPT = ChatGPT()

        with open(self.dir_path + '/train/train_dict.json') as json_file:
            self.data_dict = json.load(json_file)

        with open(self.dir_path + '/train/keywords_default.json') as json_file:
            self.keywords_dict = json.load(json_file)

    def run(self):

        try:
            # input_text = input("Mời bạn hỏi: ")
            input_text = listen_audio(self.language).lower()
            if input_text == "Keyboard Interrupted":
                return "Keyboard Interrupted"

            if (input_text == ''):
                print("input text is None")
                time.sleep(0.1)
                return "None"

            if (u"tạm biệt" in input_text) or (u"goodbye" in input_text) or (u"cảm ơn" in input_text) or (u"ありがとう" in input_text):
                if self.use_speaker:
                    if self.language == "vi":
                        text_to_speech("Tạm biệt quý khách, hẹn gặp lại quý khách.", self.language)
                    if self.language == "ja":
                        text_to_speech("さようならお客様、またお会いしましょう。", self.language)
                    if self.language == "en":
                        text_to_speech("Goodbye and see you again soon.", self.language)
                return "Done"


            # Kiểm tra từ khóa đặc biệt trong câu hỏi hay không
            have_keywords = False
            keyword_finded = ""
            for keyword_str in self.keywords_dict:
                if keyword_str in input_text:
                    have_keywords = True
                    # nếu có nhiều keyword cùng xuất hiện thì lấy keyword dài nhất
                    if len(keyword_str) > len(keyword_finded):
                        keyword_finded = keyword_str

            # nếu chatbot mkac không trả lời được
            # nếu có keyword thì trả lời theo mặc định của keyword
            if have_keywords:
                response = self.data_dict[str(self.keywords_dict[keyword_finded])]
                print("ChatBot:#", response)
                if self.use_speaker:
                    text_to_speech(response)
            else:
                # nếu không có keyword thì hỏi chatGPT
                # loại trừ những câu hỏi quá ngắn có thể do âm thanh nhiễu
                if len(input_text) < 3:
                    print("input text is short: ", len(input_text))
                    return "Short"
                # hỏi chatgpt với các câu hỏi đủ dài
                print("ChatGPT:>>")
                response = self.chatbot_GPT.ask(input_text, speak=self.use_speaker, language=self.language)
                # print(response)

        except KeyboardInterrupt:
            print ('Keyboard Interrupted1')
            return "Keyboard Interrupted"

        except:
            print("chatbot error!!!")
            if self.use_speaker:
                if self.language == "vi":
                    text_to_speech("Xin lỗi, tôi đã gặp sự cố khi tìm câu trả lời.", self.language)
                if self.language == "ja":
                    text_to_speech("申し訳ありませんが、答えを見つけるのに苦労しました。", self.language)
                if self.language == "en":
                    text_to_speech("Sorry, I had trouble finding the answer.", self.language)
            return "Error"



if __name__ == '__main__':

    chatbot_mkac = Chatbot()
    while(True):
        try:
            result = chatbot_mkac.run()
            if result == "Keyboard Interrupted" or result == "Done":
                break
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("keyboard")
            break