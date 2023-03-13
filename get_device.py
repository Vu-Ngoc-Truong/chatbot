#!/usr/bin/env python
# -*-coding:utf-8-*-
import speech_recognition as sr
r = sr.Recognizer()
for index, name in enumerate(sr.Microphone.list_microphone_names()  ):
    print('name \"{1}\" found for microphone(device={0})'.format(index,name))
    # Now, to use the Snowball microphone, you would change Microphone() to Microphone(device_index=3)