#!/usr/bin/env python
'''
Description: this function translates, speaks, and records a user-specified number of secrets from a file
Author: Rachel Kalmar

'''

import os, sys
import json
import collections
import random
import utils
from pprint import pprint
from playsound import playsound
import datetime
from six import string_types
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from pollySpeak import newSession, pollySpeech
from concatMp3 import concatMp3

USAGE_TEXT = """
Usage: secretReader.py <number of secrets to read> <voice>
"""

# Defaults (integrate this into main, and with keyword args)
from params import *

def usage():
	print(USAGE_TEXT)
	sys.exit(-1)

def main(argv):

	if len(argv) < 1:
		usage()

	# should check and make sure this is an int, and smaller than # of entries in file
	num_secrets = int(argv[0])
	print(language)

	if language=='en':
		# voiceIds = ['Joanna', 'Salli', 'Kimberly', 'Kendra', 'Amy', 'Ivy', 'Justin', 'Joey', 'Brian']
		voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']		
	elif language=='it':
		voiceIds = ['Carla', 'Giorgio']
	elif language=='de':
		voiceIds = ['Marlene', 'Hans']

	voice = argv[1]
	if voice == 'random':
		randVoice = True
	else:
		randVoice = False
		if voice not in voiceIds:
			voice = 'Joanna'

	# Load in secrets 
	secrets = []
	with open(datapath) as data_file:    
		secrets = json.load(data_file)

	# only do this is num_secrets is valid and > 0	
	# create a new folder with this timestamp to save the secret files in
	now = datetime.datetime.now()
	mp3path = '{}{}'.format(mp3path_base,now.strftime('%Y-%m-%d-%H-%M'))
	os.mkdir(mp3path)

	# create a new session
	polly = newSession()

	for i in range(0, num_secrets):
		# Choose a new secret 
		if shuffleSecrets:
			idx = random.randint(0,len(secrets))
		else:
			idx = i
		secret = utils.convertUnicode(secrets[idx])
		pprint(secret)

		# Skip this secret if it isn't slated for publishing
		if not secret['publish']:
			continue

		# Choose voice
		if randVoice:
			voiceId = random.choice(voiceIds)
			print(voiceId)
		else:
			voiceId = voice

		# Prepare secret
		if translate_lang:
			translation = translate_client.translate(secret['text'], target_language=target_lang, format_='text')
			secretText = translation['translatedText']
		elif language == 'it':
			secretText = secret['italianString']
		elif language == 'de':
			secretText = secret['germanString']
		elif language == 'en':
			secretText = secret['englishString']

		if ssml:
			secretText = utils.createSSML(secretText, sentencePause=True, whisper=False)
		else:
			secretText = secret['text']

		# Speak and record secret
		pollySpeech(
			polly,
			text=secretText,
			textType=textType,
			voiceId=voiceId,
			outputFile='{}/secret-{}'.format(mp3path,i),
			speak=True)

	# Merge all secret mp3s into one merged mp3
	print('Now concatenating mp3s...')
	concatMp3(mp3path + '/', mp3_padding)

if __name__ == "__main__":
	main(sys.argv[1:])

