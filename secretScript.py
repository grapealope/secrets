import os, sys
import json
import csv
import collections
import random
from pprint import pprint
from playsound import playsound
import datetime
from six import string_types
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from pollySpeak import newSession, pollySpeech
from concatMp3 import concatMp3
from nltk import tokenize
from google.cloud import translate

import utils
from utils import createTimestampedDir
from pollySpeak import newSession, pollySpeech, speakSecrets

# Defaults (integrate this into main, and with keyword args)
from params import *

datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_edit_italian.json'

secrets = []
with open(datapath) as data_file:    
	secrets = json.load(data_file)


italian_secrets = [secret for secret in secrets if secret['language'] == 'it' and secret['publish']]
english_secrets = [secret for secret in secrets if secret['language'] == 'en' and secret['publish']]

# Note: secret 137 breaks the code with its <3, kludgey fix for now
english_secrets[137]['englishString'] = 'I still love my first love'

# ------------------------------------------ #
# English 

voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']

speakSecrets(english_secrets[0:70], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[70:140], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[140:210], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[210:280], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[280:], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)


# ------------------------------------------ #
# Italian 

voiceIds = ['Carla', 'Giorgio']
 
speakSecrets(italian_secrets[0:50], voiceIds, createTimestampedDir(mp3path_base),
				 randVoice=True,
				 language='it', 
				 target_lang='it')

speakSecrets(italian_secrets[50:100], voiceIds, createTimestampedDir(mp3path_base),
				 randVoice=True,
				 language='it', 
				 target_lang='it')

speakSecrets(italian_secrets[100:], voiceIds, createTimestampedDir(mp3path_base),
				 randVoice=True,
				 language='it', 
				 target_lang='it')

# ------------------------------------------ #
# Fix timing

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-25'
concatMp3(mp3path + '/', file_padding=mp3_padding)

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-43'
concatMp3(mp3path + '/', file_padding=mp3_padding)

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-48'
concatMp3(mp3path + '/', file_padding=mp3_padding)

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-52'
concatMp3(mp3path + '/', file_padding=mp3_padding)




