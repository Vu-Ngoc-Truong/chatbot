#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import playsound
from gtts import gTTS
# import time
# import sys

def text_to_speech(text, language='vi'):
    if text == None or text == "":
        return
    try:
        output = gTTS(text,lang=language, slow=False)
        output.save("output.mp3")
        playsound.playsound('output.mp3', True)
        os.remove("output.mp3")
    except:
        print("text to speech error")

if __name__ == '__main__':
    text_to_speech("Xin chào, tôi có thể giúp gì cho bạn?")