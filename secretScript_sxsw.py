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

csvfile = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_sxsw_sn_curated.csv'
datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_sxsw.json'

createSecretsJsonFromCSV(csvfile, datapath)

secrets = []
with open(datapath) as data_file:    
	secrets = json.load(data_file)

voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian', 'Matthew', 'Nicole', 'Russell']
whisperFreq = 0.2			# What percentage of the secrets should be whispered?
# attenuations_list = [0, 2.5, 5, 7.5, 10]
# attenuations_list = [0, 2, 4, 6, 8]
# attenuations_list = [0, 1, 2, 3, 4]
attenuations_list = [0]
random_min = 1000
random_max = 4000
secrets_per_file = 195


# Shuffle secrets
random.shuffle(secrets)
secrets[0:10]

mp3path = createTimestampedDir(mp3path_base)
speakSecrets(secrets, voiceIds, mp3path, whisperFreq=0.15, randVoice=True, mp3_padding='random',
			 createLog=True, attenuation_list=attenuations_list)

concatMp3(mp3path + '/', file_name='mergedSecrets-group-{}'.format(0), file_padding='random', random_min=1000, random_max=4000, verbose=True)

for fdx in range(0,5):
	range_start = fdx * secrets_per_file
	range_stop = range_start + secrets_per_file
	print('{} range: {}-{}'.format(fdx, range_start, range_stop))
	concatMp3(mp3path + '/', file_name='mergedSecrets-group-{}'.format(fdx), file_padding='random', random_min=1000, random_max=4000,
		range_start=range_start, range_stop=range_stop, verbose=True)	

# ------------------------------------------ #
# Test voices

mp3path = createTimestampedDir(mp3path_base)
attenuations_list = [0]

voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']
voiceIds = ['Salli', 'Kimberly', 'Justin', 'Emma', 'Nicole', 'Russell', 'Matthew', 'Geraint', 'Celine', 
			'Mathieu', 'Chantal', 'Hans', 'Marlene', 'Vicki', 'Ricardo', 'Vitoria', 'Miguel', 'Penelope', 
			'Astrid', 'Maxim', 'Tatyana', 'Carla', 'Giorgio']

for voiceId in voiceIds:
	speakSecrets([secrets[1]], [voiceId], mp3path, whisperFreq=0, randVoice=False, outputFileIdx=voiceId,
				 createLog=False, attenuation_list=attenuations_list)

# ------------------------------------------ #
# English 

voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']

speakSecrets(english_secrets[0:70], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[70:140], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[140:210], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[210:280], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[280:], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)

speakSecrets(english_secrets[137:138], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)
speakSecrets(english_secrets[138:139], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)


speakSecrets(english_secrets[0:500], voiceIds, createTimestampedDir(mp3path_base), randVoice=True, verbose=True)


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

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-11-10-test'
concatMp3(mp3path + '/', file_padding=45000)
concatMp3(mp3path + '/', file_padding='random')

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-11-10-1'
concatMp3(mp3path + '/', file_padding='random')

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-11-10-2'
concatMp3(mp3path + '/', file_padding='random')

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-11-10-3'
concatMp3(mp3path + '/', file_padding='random')

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-11-10-4'
concatMp3(mp3path + '/', file_padding='random')

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-11-10-5'
concatMp3(mp3path + '/', file_padding='random')

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-25'
concatMp3(mp3path + '/', file_padding=mp3_padding)

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-43'
concatMp3(mp3path + '/', file_padding=mp3_padding)

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-48'
concatMp3(mp3path + '/', file_padding=mp3_padding)

mp3path = '/Users/kalmar/Documents/code/secrets/audio/2017-05-20-03-52'
concatMp3(mp3path + '/', file_padding=mp3_padding)




