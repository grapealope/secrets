#!/usr/bin/env python
'''
Description: pieces of code to create mp3 files saying 'danke' with different German voices
Author: Rachel Kalmar 

'''
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from pprint import pprint
from playsound import playsound
import utils
import random
from concatMp3 import concatMp3

# Defaults (integrate this into main, and with keyword args)
from params import *

mp3path = utils.createTimestampedDir(mp3path_base)

polly = newSession()
pollySpeech(polly, text='Danke', voiceId='Vicki', speak=True, outputFile='{}/danke-vicki'.format(mp3path))
pollySpeech(polly, tex t='Danke', voiceId='Hans', speak=True, outputFile='{}/danke-hans'.format(mp3path))
pollySpeech(polly, text='Danke', voiceId='Marlene', speak=True, outputFile='{}/danke-marlene'.format(mp3path))


import os
import glob
import utils
from random import randint
from pydub import AudioSegment

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2018-01-10-23-51/'
# mp3_file = 'danke-hans.mp3'
# file_name = 'danke-hans'
# mp3_file = 'danke-vicki.mp3'
# file_name = 'danke-vicki'
mp3_file = 'danke-marlene.mp3'
file_name = 'danke-marlene'

os.chdir(mp3path)
audio_secret = AudioSegment.from_mp3(mp3_file)
	
print(mp3path,file_name)
fname = utils.createUniqueFilename(mp3path + file_name + '.wav')

with open(fname, 'wb') as f:
	audio_secret.export(fname, format='wav')
