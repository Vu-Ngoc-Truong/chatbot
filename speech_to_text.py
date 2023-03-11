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
        self.energy_threshold = 1000  # Ngưỡng năng lượng để xác định có lấy âm hay không.
        self.pause_threshold = 1.5 # Thời gian xác nhận đã dừng nói để kết thúc nghe.
        self.dynamic_energy_threshold = True  # Tự động xác định ngưỡng năng lượng
        # c.operation_timeout = 20 # Thời gian tối đa (theo giây) mà một hoạt động (ví dụ: yêu cầu API) có thể chạy trước khi hết thời gian chờ. Nếu giá trị được thiết lập là None, thì không có giới hạn thời gian chờ.

    def listen(self, language='vi'):
        try:
            with sr.Microphone() as source: # Lấy nguồn nói từ Microphone

                self.c.adjust_for_ambient_noise(source, duration= 2.0)
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
                if self.use_ROS:
                    self.pub.publish("LISTEN")
                playsound.playsound(self.dir_path+ '/logon.mp3', True)
                print('Listening...')
                try:
                    audio = self.c.listen(source,timeout=10, phrase_time_limit= 20) # Biến audio là giá trị dạng chuỗi sau khi máy nghe và nhận dạng từ nguồn vào
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
            return ''
        except KeyboardInterrupt:
            print ('Keyboard Interrupted')
            return 'Keyboard Interrupted'

def listen_audio(language='vi', use_ROS=False, auto_language=False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if use_ROS:
        import rospy
        from std_msgs.msg import String
        pub = rospy.Publisher('chatbot_status', String, queue_size=10)

    languages_list = ["vi", "en", "ja"]
    # print(dir_path)
    c = sr.Recognizer() # Khởi tạo biến nhận dạng giọng nói
    c.energy_threshold = 1000  # Ngưỡng năng lượng để xác định có lấy âm hay không.
    c.pause_threshold = 1.5 # Thời gian xác nhận đã dừng nói để kết thúc nghe.
    c.dynamic_energy_threshold = True  # Tự động xác định ngưỡng năng lượng
    # c.operation_timeout = 20 # Thời gian tối đa (theo giây) mà một hoạt động (ví dụ: yêu cầu API) có thể chạy trước khi hết thời gian chờ. Nếu giá trị được thiết lập là None, thì không có giới hạn thời gian chờ.
    try:
        with sr.Microphone() as source: # Lấy nguồn nói từ Microphone

            c.adjust_for_ambient_noise(source, duration= 2.0)
            # for count in range(5):
            #     c.adjust_for_ambient_noise(source, duration= 4.0)
            #     print("energy_threshold: ", c.energy_threshold)
            #     count +=1
            #     if c.energy_threshold < 2000:
            #         break
            # if c.energy_threshold > 2000:
            #     return "None"
            print("energy_threshold: ", c.energy_threshold)
            # buffer = source.stream.read(source.CHUNK)
            # energy = audioop.rms(buffer, source.SAMPLE_WIDTH)  # energy of the audio signal
            # print("energy: ", energy)
            # seconds_per_buffer = (source.CHUNK + 0.0) / source.SAMPLE_RATE
            # damping = c.dynamic_energy_adjustment_damping ** seconds_per_buffer  # account for different chunk sizes and rates
            # print("damping: ", damping )
            if use_ROS:
                pub.publish("LISTEN")
            playsound.playsound(dir_path+ '/logon.mp3', True)
            print('Listening...')
            try:
                audio = c.listen(source,timeout=10, phrase_time_limit= 20) # Biến audio là giá trị dạng chuỗi sau khi máy nghe và nhận dạng từ nguồn vào
                playsound.playsound(dir_path+ '/logoff.mp3', True)
                # cropped_audio = audio.get_segment(0, 4000) # cắt lấy 5 giây đầu tiên
                # with open("recording.wav", "wb") as f:
                #     f.write(cropped_audio.get_wav_data())

                # # Auto detect language
                # if auto_language:
                #     confidences = []
                #     query_list = []
                #     len_query_list = []
                #     start_time = time.time()

                #     for lang in languages_list:
                #         try:
                #             results = c.recognize_google(cropped_audio, language=lang, show_all=True)
                #             # print("query:", results)
                #             if "alternative" in results:
                #                 query_ = results['alternative'][0]['transcript']
                #                 confidence = results['alternative'][0]['confidence']

                #             else:
                #                 query_ = ""
                #                 confidence = 0

                #         except:
                #             print("Could not understand audio")
                #             query_ = ""
                #             confidence = 0

                #         confidences.append(confidence)
                #         query_list.append(query_)
                #         len_query_list.append(len(query_))

                #     elapsed_time = time.time() - start_time
                #     print("Time2:", elapsed_time)
                #     print(query_list)
                #     print(len_query_list)
                #     print(confidences)
                #     # print(lang_result_list)
                #     index_min = len_query_list.index(min(len_query_list))
                #     confidences[index_min] = 0
                #     index = confidences.index(max(confidences))
                #     language = languages_list[index]
                #     print("Language is: ", language)

                # Recognizing audio file
                if use_ROS:
                    pub.publish("RECOG")
                print("Recognizing")
                query = c.recognize_google(audio, language=language)
                print("Customer: ",query)
            except sr.WaitTimeoutError:
                if use_ROS:
                    pub.publish("TIMEOUT")
                playsound.playsound(dir_path+ '/logoff.mp3', True)
                print("WaitTimeoutError")
                return ''

        return query # Tra ve text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ''
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ''
    except KeyboardInterrupt:
        print ('Keyboard Interrupted')
        return 'Keyboard Interrupted'


def giao_tiep_voi_khach():

    reg_audio = ListenAudio(use_ROS=True)
    while(True):

        try:
            query = reg_audio.listen("vi").lower()
            if query == "Keyboard Interrupted" or ("goodbye" in  query):
                return
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("keyboard")
            break

if __name__ == '__main__':

    giao_tiep_voi_khach()
