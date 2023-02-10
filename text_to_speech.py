#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import playsound
from gtts import gTTS
# import time
# import sys
# import wikipedia
# wikipedia.set_lang('vi')

def text_to_speech(text, language='vi'):
    output = gTTS(text,lang=language, slow=False)
    output.save("output.mp3")
    playsound.playsound('output.mp3', True)
    os.remove("output.mp3")

if __name__ == '__main__':
    text_to_speech("Xin chào, tôi có thể giúp gì cho bạn?")