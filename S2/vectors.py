#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import subprocess
'''
I just realised that I was working with the wrong version of the BBB video, so from now on 
I will be using the full version.
'''
class p2:

    def __init__(self):
        self.movie = "bbb_full.mp4"

    def macroblocks(self):
        os.system('ffmpeg -flags2 +export_mvs -i cut.mp4 -vf codecview=mv=pf+bf+bb output.mp4')
        print("sucess")

    def container(self):
        if not os.path.exists("oneminute.mp4"):
            os.system('ffmpeg -ss 0 -i ' + self.movie + ' -c copy -t 60 oneminute.mp4')
        #export mp3 stero track
        if not os.path.exists("stereo-audio.mp3"):
            os.system('ffmpeg -i oneminute.mp4 -map 0:a -acodec mp3 -joint_stereo 1 stereo-audio.mp3')
        # export aac audio with lower bit rate (128k - is already pretty low?)
        if not os.path.exists("aac-audio.aac"):
            os.system('ffmpeg -i oneminute.mp4 -map 0:a -acodec aac aac-audio.aac')
        os.system('ffmpeg -i oneminute.mp4 -i stereo-audio.mp3 -i aac-audio.aac -map 0:v -map 1:a -map 2:a -c copy container.mp4')
        print("sucess(?)")
        #somehow the .mp4 file is not playable but I don't know why...


    #hard coded version for an mp4 file with two audio streams and one video stream
    def broadcast(self):
        possiblebroadcasts = []
        video = subprocess.check_output('ffprobe -v error -select_streams v -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 container.mp4', stderr=subprocess.STDOUT, shell=True)[:-1]
        audio = subprocess.check_output('ffprobe -v error -select_streams a -show_entries stream=codec_name \
          -of default=noprint_wrappers=1:nokey=1 container.mp4', stderr=subprocess.STDOUT, shell=True)
        audio = [audio[:-5], audio[4:-1]]
        print(video, audio)

        if video in [b'h264', b'MPEG2', b'AVS', b'AVS+']:
            if audio[1] or audio[2] in [b'mp3', b'aac', b'ac-3']:
                possiblebroadcasts.append("DTMB")
        if video in[b'h264', b'MPEG2']:
            if audio[1] or audio[2] in[b'mp3', b"aac", b"ac-3"]:
                possiblebroadcasts.append("DVB")
            if audio[1] or audio[2] in [b"ac-3"]:
                possiblebroadcasts.append("ATSC")
            if audio[1] or audio[2] in [b"aac"]:
                possiblebroadcasts.append("ISDB")
        else:
            possiblebroadcasts.append("error")
        print("possible broadcasting standards would be: " + str(possiblebroadcasts))

    def subtitles(self):
        os.system('ffmpeg -i ' + self.movie + ' -vf subtitles=subtitles.srt mysubtitledmovie.mp4')
        print("sucess")

p = p2()
#p.macroblocks()
#p.container()
#p.broadcast()
p.subtitles()

