#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys
import speech_recognition as sr
import time
import playsound
HOME = os.path.expanduser('~')
class ListenAudio:
    def __init__(self, use_ROS=False, auto_language=False):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.use_ROS = use_ROS
        languages_list = ["vi", "en", "ja"]

        if self.use_ROS:
            import rospy
            from std_msgs.msg import String
            self.pub = rospy.Publisher('chatbot_status', String, queue_size=10)
        # print(dir_path)
        self.c = sr.Recognizer() # Khởi tạo biến nhận dạng giọng nói
        self.energy_threshold = 300  # Ngưỡng năng lượng để xác định có lấy âm hay không.
        self.pause_threshold = 1.5 # Thời gian xác nhận đã dừng nói để kết thúc nghe.
        self.dynamic_energy_threshold = True  # Tự động xác định ngưỡng năng lượng
        # c.operation_timeout = 20 # Thời gian tối đa (theo giây) mà một hoạt động (ví dụ: yêu cầu API) có thể chạy trước khi hết thời gian chờ. Nếu giá trị được thiết lập là None, thì không có giới hạn thời gian chờ.

    def listen(self, language='vi'):
        try:
            with sr.Microphone() as source: # Lấy nguồn nói từ Microphone

                self.c.adjust_for_ambient_noise(source, duration= 3.0)
                # for count in range(5):
                #     c.adjust_for_ambient_noise(source, duration= 4.0)
                #     print("energy_threshold: ", c.energy_threshold)
                #     count +=1
                #     if c.energy_threshold < 2000:
                #         break
                # if c.energy_threshold > 2000:
                #     return "None"
                print("energy_threshold: ", self.c.energy_threshold)
                # buffer = source.stream.read(source.CHUNK)
                # energy = audioop.rms(buffer, source.SAMPLE_WIDTH)  # energy of the audio signal
                # print("energy: ", energy)
                # seconds_per_buffer = (source.CHUNK + 0.0) / source.SAMPLE_RATE
                # damping = c.dynamic_energy_adjustment_damping ** seconds_per_buffer  # account for different chunk sizes and rates
                # print("damping: ", damping )
                playsound.playsound(self.dir_path+ '/logon.mp3', True)
                print('Listening...')
                if self.use_ROS:
                    self.pub.publish("LISTEN")
                try:
                    start_time = time.time()
                    audio = self.c.listen(source,timeout=8, phrase_time_limit= 12) # Biến audio là giá trị dạng chuỗi sau khi máy nghe và nhận dạng từ nguồn vào
                    elapsed_time = time.time() - start_time
                    # print(audio.sample_width) # get sample width
                    # print(audio.sample_rate)  # get sample rate
                    # print("listen time: ", elapsed_time)
                    if elapsed_time < 2.0:
                        print("audio short")
                        # print(type(audio))
                        try:
                            audio2 = self.c.listen(source,timeout=5, phrase_time_limit= 10) # Biến audio là giá trị dạng chuỗi sau khi máy nghe và nhận dạng từ nguồn vào
                            # # Ghép hai chuỗi audio lại với nhau
                            audio_byte = audio.get_raw_data(convert_rate=44100,convert_width=2) + audio2.get_raw_data(convert_rate=44100,convert_width=2) # convert_rate=40,convert_width=1
                            audio = sr.AudioData(audio_byte, sample_rate=44100, sample_width=2)
                            # print(type(audio))
                        except:
                            pass

                    playsound.playsound(self.dir_path+ '/logoff.mp3', True)

                    # Recognizing audio file
                    if self.use_ROS:
                        self.pub.publish("RECOG")
                    print("Recognizing")
                    query = self.c.recognize_google(audio, language=language)
                    print("Customer: ",query)
                except sr.WaitTimeoutError:
                    if self.use_ROS:
                        self.pub.publish("TIMEOUT")
                    playsound.playsound(self.dir_path+ '/logoff.mp3', True)
                    print("WaitTimeoutError")
                    return ''

            return query # Tra ve text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ''
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            if self.use_ROS:
                self.pub.publish("WIFI_ERROR")
            return ''
        except KeyboardInterrupt:
            print ('Keyboard Interrupted')
            return 'Keyboard Interrupted'

if __name__ == '__main__':

    reg_audio = ListenAudio(use_ROS=False)
    while(True):

        try:
            query = reg_audio.listen("en").lower()
            if (query == "Keyboard Interrupted") or ("goodbye" in  query) or (u"ありがとう" in query):
                break
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("keyboard")
            break
