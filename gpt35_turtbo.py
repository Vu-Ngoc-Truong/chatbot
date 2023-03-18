#!/usr/bin/env python3
# -*-coding:utf-8-*-

from text_to_speech import text_to_speech
from speech_to_text import ListenAudio
import json
import yaml
import os
import time
import openai

# API Key
openai.api_key = os.environ.get('OPENAI_API_KEY')
# print(openai.api_key)
# organization of MEIKO
# openai.organization = "org-ORyxAR79nusDu86NyNXgXtC4"

class Chatbot:
    def __init__(self, language='vi', use_speaker=True, use_ROS=False, max_tokens_ans=300):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.language = language
        self.use_speaker = use_speaker
        self.use_ROS = use_ROS
        self.led_effect = "INIT"
        self.listen_audio = ListenAudio(True)
        if self.use_ROS:
            import rospy
            from std_msgs.msg import String
            self.pub = rospy.Publisher('chatbot_status', String, queue_size=10)
            # rospy.init_node('chatbot_talk')
            self.pub.publish(self.led_effect)

        # Number of user and assistant message is saved in conversation, if =0 is save all message
        self.history_length = 1
        self.max_tokens_ans = max_tokens_ans

        self.vi_short_msg = ".Trả lời ngắn dưới " + str(self.max_tokens_ans) + " tokens bằng tiếng Việt"
        self.en_short_msg = ".Short answer under " + str(self.max_tokens_ans) + " tokens in English"
        self.ja_short_msg = "。日本語で " + str(self.max_tokens_ans) + " トークン未満の短い回答。"

        self.vi_trans_str_list = ["can you speak vietnamese", "ベトナム語を話せますか", "bạn có thể nói tiếng việt không","bạn có thể nói được tiếng việt không"]
        self.vi_confirm = "Vâng, tôi có thể nói tiếng Việt. Bạn cần tôi giúp gì không?"
        self.en_trans_str_list = ["can you speak english", "bạn có thể nói tiếng anh không","bạn có thể nói được tiếng anh không", "英語を話せますか"]
        self.en_confirm = "Yes, I can speak English. How can I assist you?"
        self.ja_trans_str_list = ["can you speak japanese", "bạn có thể nói tiếng nhật không", "bạn có thể nói được tiếng nhật không","日本語を話せますか"]
        self.ja_confirm = "はい、私は日本語を話すことができます。"
        # Creat language dict data
        self.language_dict = {}
        self.language_dict["vi"] = {"trans_str": self.vi_trans_str_list, "confirm_str": self.vi_confirm, "short_str": self.vi_short_msg}
        self.language_dict["en"] = {"trans_str": self.en_trans_str_list, "confirm_str": self.en_confirm, "short_str": self.en_short_msg}
        self.language_dict["ja"] = {"trans_str": self.ja_trans_str_list, "confirm_str": self.ja_confirm, "short_str": self.ja_short_msg}
        # print(self.language_dict)

        # Set the behavior of the assistant, instructed with "You are a helpful assistant."
        self.conversation=[{"role": "system", "content": "You are a helpful assistant.Short answer under 300 tokens."}]

        with open(self.dir_path + '/train/train_dict.json') as json_file:
            self.data_dict = json.load(json_file)

        with open(self.dir_path + '/train/keywords_default.json') as json_file:
            self.keywords_dict = json.load(json_file)

    def text_to_speech(self, text, language="vi"):
        self.pub.publish("PLAY_SOUND")
        text_to_speech(text, language)

    def run(self, use_mic=True):
        try:
            #####  Get input ask  ########
            if use_mic:
                print("language ask:", self.language)
                input_text = self.listen_audio.listen( self.language).lower()
            else:
                input_text = input("Mời bạn hỏi: ")

            if input_text == "Keyboard Interrupted":
                return "Keyboard Interrupted", None

            if (input_text == ''):
                print("input text is None")
                time.sleep(0.1)
                return "None", None

            # Transfer to other language
            change_language = False
            for lang in self.language_dict:
                for lang_trans_str in self.language_dict[lang]["trans_str"]:
                    if lang_trans_str in input_text:
                        print(lang_trans_str)
                        if self.language != lang:
                            print("change language: {} --> {}".format(self.language, lang))
                            self.language = lang
                            change_language = True
                            self.text_to_speech(self.language_dict[lang]["confirm_str"], self.language)
                            return "Change Language", lang
                        else:
                            print("confirm language: ", lang)
                            self.text_to_speech(self.language_dict[lang]["confirm_str"], self.language)
                            return "Confirm Language", None

            # Check break condition
            if (u"goodbye" in input_text) or (u"cảm ơn" in input_text) or (u"ありがとう" in input_text):
                if self.use_speaker:
                    if self.language == "vi":
                        self.text_to_speech("Tạm biệt quý khách, hẹn gặp lại quý khách.", self.language)
                    if self.language == "ja":
                        self.text_to_speech("さようならお客様、またお会いしましょう。", self.language)
                    if self.language == "en":
                        self.text_to_speech("Goodbye and see you again soon.", self.language)
                return "Done",None

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
                    self.text_to_speech(response, self.language)
            else:
                # nếu không có keyword thì hỏi chatGPT
                # # loại trừ những câu hỏi quá ngắn có thể do âm thanh nhiễu
                # if len(input_text) < 3:
                #     print("input text is short: ", len(input_text))
                #     return "Short"
                # hỏi chatgpt với các câu hỏi đủ dài
                ask_str = input_text + self.language_dict[self.language]["short_str"]
                print("ask string: ", ask_str)
                self.conversation.append({"role": "user", "content": ask_str})
                print("ChatGPT:>>")

                # Creat chatbot GPT 3.5 turbo
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0301",
                    messages = self.conversation,
                    temperature=1.0,
                    max_tokens=self.max_tokens_ans+10,
                    top_p=0.9
                )
                # for choice in response['choices']:
                #     print("\n" + choice['message']['content'] + "\n")

                # add assistant messages to conversation
                self.conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
                # Cut history
                while ( self.history_length > 0) and (len(self.conversation) > (2*self.history_length +1)) or (len(self.conversation) > 7):
                    # Remove user message
                    self.conversation.pop(1)
                    # Remove assistant message
                    self.conversation.pop(2)
                    # print("Cut history, conversison lenth is ", len(self.conversation))
                answer = response['choices'][0]['message']['content']
                # print(response)
                if self.use_ROS:
                    self.led_effect = "ANSWER"
                    self.pub.publish(self.led_effect)
                # print(response['usage'])
                print("GPT-3.5: ", answer)
                if self.use_speaker:
                    self.text_to_speech(answer, self.language)

        except KeyboardInterrupt:
            print ('Keyboard Interrupted1')
            return "Keyboard Interrupted", None

        except Exception as e:
            print("chatbot error: ", e )
            if self.use_ROS:
                self.led_effect = "ERROR"
                self.pub.publish(self.led_effect)
            if self.use_speaker:
                if self.language == "vi":
                    self.text_to_speech("Xin lỗi, tôi đã gặp sự cố khi tìm câu trả lời.", self.language)
                if self.language == "ja":
                    self.text_to_speech("申し訳ありませんが、答えを見つけるのに苦労しました。", self.language)
                if self.language == "en":
                    self.text_to_speech("Sorry, I had trouble finding the answer.", self.language)
            return "Error", None


if __name__ == '__main__':

    chatbot_mkac = Chatbot(use_speaker=False,use_ROS=False)
    while(True):
        try:
            result = chatbot_mkac.run()
            if result == "Keyboard Interrupted" or result == "Done":
                break
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("keyboard")
            break
