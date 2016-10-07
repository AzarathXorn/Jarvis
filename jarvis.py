#!/usr/bin/python3

# Written by William Schultz

# A program to listen to the user and search youtube for music
# for personal use as a "virtual home DJ" of sorts
# using the speech recognition library from
# https://pypi.python.org/pypi/SpeechRecognition

import speech_recognition as sr
import re
import urllib.parse
import urllib.request
import pafy
import vlc
import time
import sys
# import datetime
# import pyttsx

# instantiate the speech recognizer, and set the threshold 
r = sr.Recognizer()
r.energy_threshold = 1100

mic = sr.Microphone()
# just uses the system's default microphone

with mic as source:
    print("Say the name of a song I should play!")
    audio = r.listen(source)
    print("Heard you! Processing...\n")

# recognize speech using Google Speech Recognition
try:
    result = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said: " + result)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    sys.exit()
except sr.RequestError as e:
    print("""Could not request results from Google 
        Speech Recognition service; {0}""".format(e))
    sys.exit()

# encode result into search url, find first result, then return link
# urllib and re method inspired by
# goo.gl/jqdks7  (stackechange question on this topic)
qstr = urllib.parse.urlencode({"search_query" : result})
rawhtml = urllib.request.urlopen("http://www.youtube.com/results?" 
                                    + qstr)
srch_results = re.findall(r'href=\"\/watch\?v=(.{11})', 
                            rawhtml.read().decode())
url = ("http://www.youtube.com/watch?v=" + srch_results[0])
# This could probably be cut down without findall
print(url + "\n")
vid = pafy.new(url)
vidlen = vid.length
bestaudio = vid.getbestaudio()
vidsource = bestaudio.url
# print(bestaudio.url + "\n")
# bestaudio.download('C:\\Users\\Will\\Documents\\Jarvis')
# print(type(vidsource))
p = vlc.MediaPlayer(vidsource)
p.play()
p.audio_set_volume(40)
time.sleep(vidlen)
