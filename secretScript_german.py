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

# Do this in Python 2 to get around unicode issue
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Defaults (integrate this into main, and with keyword args)
from params import *

# datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_edit_italian.json'
# datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_english.json'
# datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_edit_german_new.json'
datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_german_berlin.json'

secrets = []
with open(datapath) as data_file:    
	secrets = json.load(data_file)

frequency_german = 0.7
whisperFreq = 0.15
secrets_per_file = 70

tally_de = 0
tally_en = 0
for secret in secrets:
	if secret['language'] == '':
		die_roll = random.random()
		if  die_roll < frequency_german:
			secret['language'] = 'de'
			tally_de += 1
		else:
			secret['language'] = 'en'
			tally_en += 1
	elif secret['language'] == 'de':
		tally_de += 1
	elif secret['language'] == 'en':
		tally_en += 1
	else:
		print("language '{}' is invalid!".format(secret['language']))
print(tally_de, tally_en)

german_secrets = [secret for secret in secrets if secret['language'] == 'de' and secret['publish']]
english_secrets = [secret for secret in secrets if secret['language'] == 'en' and secret['publish']]

random.shuffle(german_secrets)
random.shuffle(english_secrets)

german_secrets = german_secrets[0:140]
english_secrets = english_secrets[0:60]

# make list of german secrets and english secrets
# each pass through the loop, randomly speak and remove one secret from either queue
# continue until all secrets have been used

mp3path = createTimestampedDir(mp3path_base)
fdx = 0
idx = 0
done = False
secrets_done = False
while not done:
	# roll a die, if value is less than the threshold, speak a german secret 
	die_roll = random.random()
	if  die_roll < frequency_german and len(german_secrets) > 0:
		print(fdx, idx, 'de')
		# choose a random secret from the list of german secrets
		secret = german_secrets.pop()
		speakSecrets([secret], germanVoiceIds, mp3path, language='de', whisperFreq=whisperFreq, concatSecretMp3s=False, outputFileIdx=idx)	
		idx+=1
	elif die_roll >= frequency_german and len(english_secrets) > 0:
		print(fdx, idx, 'en')
		secret = english_secrets.pop()
		speakSecrets([secret], englishVoiceIds, mp3path, language='en', whisperFreq=whisperFreq, concatSecretMp3s=False, outputFileIdx=idx)	
		idx+=1	
	secrets_done = (len(german_secrets) == 0) and (len(english_secrets) == 0)
	if (idx % secrets_per_file == 0) or secrets_done:
		range_start = fdx * secrets_per_file
		range_stop = idx-1
		print('range: {}-{}'.format(range_start, range_stop))
		print('mergedSecrets-{}'.format(fdx))
		# concatMp3(mp3path + '/', file_name='mergedSecrets-{}'.format(fdx), file_padding='random', range_start=range_start, range_stop=range_stop, verbose=True)		
		concatMp3(mp3path + '/', file_name='mergedSecrets-{}'.format(fdx), file_padding='random', random_min=3000, random_max=40000,
			range_start=range_start, range_stop=range_stop, verbose=True)
		fdx+=1
	if secrets_done:
		done = True

for fdx in range(0,8):
	range_start = fdx * secrets_per_file
	range_stop = range_start + secrets_per_file
	print('{} range: {}-{}'.format(fdx, range_start, range_stop))
	concatMp3(mp3path + '/', file_name='mergedSecrets-padded-10-{}'.format(fdx), file_padding='random', random_min=1500, random_max=10000,
		range_start=range_start, range_stop=range_stop, verbose=True)		


# ------------------------------------------ #
# English 

voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']

speakSecrets(english_secrets[0:70], voiceIds, createTimestampedDir(mp3path_base), randVoice=True)


# ------------------------------------------ #
# German

# make list of german secrets and english secrets
# each pass through the loop, randomly speak and remove one secret from either queue
# continue until all secrets have been used

voiceIds = ['Vicki', 'Marlene', 'Hans']

speakSecrets(secrets[0:15], voiceIds, createTimestampedDir(mp3path_base),
				 randVoice=True,
				 language='de', 
				 target_lang='de')

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




