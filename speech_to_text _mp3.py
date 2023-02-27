#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys
import speech_recognition as sr
import time
import audioop
import playsound
HOME = os.path.expanduser('~')
from pydub import AudioSegment
import langid

def convert_mp3_to_wav(mp3_file):
    sound = AudioSegment.from_mp3(mp3_file)
    wav_file = mp3_file.replace(".mp3", ".wav")
    sound.export(wav_file, format="wav")
    return wav_file


def listen_audio(language='vi', file_name=""):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    # Tạo một đối tượng recognizer
    c = sr.Recognizer() # Khởi tạo biến nhận dạng giọng nói
    languages = ["vi", "en", "ja"]
    langid.set_languages(languages)
    confidences = []
    try:
        audio_path = dir_path + "/audio_test/"+ file_name + ".mp3"
        print(audio_path)
        # playsound.playsound(audio_path, True)
        # Đọc file âm thanh
        audio_file = sr.AudioFile(convert_mp3_to_wav(audio_path))
        with audio_file as source:
            audio = c.record(source, duration=3)
        print("Recognizing")
        # nhan dang tieng viet thi dung 'vi'
        query_list = []
        lang_result_list = []
        start_time = time.time()

        for lang in languages:
            try:
                results = c.recognize_google(audio, language=lang, show_all=True)
                print("query:", results)
                if "alternative" in results:
                    query_ = results['alternative'][0]['transcript']
                    confidence = results['alternative'][0]['confidence']
                else:
                    query_ = ""
                    confidence = 0
                query_list.append(query_)
                confidences.append(confidence)
            except sr.UnknownValueError:
                print("Could not understand audio")
                query_list.append("")
                confidences.append(-10000)
                lang_result_list.append("")


        elapsed_time = time.time() - start_time
        print("Time2:", elapsed_time)
        print(query_list)
        print(confidences)
        # print(lang_result_list)
        index = confidences.index(max(confidences))
        print("Language is: ", languages[index])
        query = query_list[index]
        # print("Customer: ",query)

        return query # Tra ve text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return 'None'
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return 'None'
    except KeyboardInterrupt:
        print ('Keyboard Interrupted')
        return 'Keyboard Interrupted'


def giao_tiep_voi_khach():

    while(True):

        try:
            input_text = input("File Name: ")
            query = listen_audio(file_name= input_text).lower()
            if query == "Keyboard Interrupted" or query == "goodbye":
                return
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("keyboard")
            break

if __name__ == '__main__':

    giao_tiep_voi_khach()
