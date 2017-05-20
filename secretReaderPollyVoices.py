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
from pollySpeak import newSession, pollySpeech, speakSecrets
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

	# should check and make sure this is an int
	num_secrets = int(argv[0])
	print(language)

	voice = argv[1]
	if voice == 'random':
		randVoice = True
	else:
		randVoice = False
		if voice not in voiceIds:
			voice = voiceIds[0]

	# Load in secrets 
	secrets = []
	with open(datapath) as data_file:    
		secrets = json.load(data_file)

	# only do this is num_secrets is valid and > 0	
	if len(secrets) == 0:
		print('Error: no secrets loaded. Please check the file referenced in params.py.')
		sys.exit(-1)
	if num_secrets == 0:
		print('Error: no secrets requested.')
		usage()
		sys.exit(-1)
	if num_secrets > len(secrets):
		print('Warning: number of secrets requested > number of secrets available ({} requested, {} available)'.format(num_secrets,len(secrets)))

	# create a new folder with this timestamp to save the secret files in
	mp3path = utils.createTimestampedDir(mp3path_base)

	speakSecrets(secrets[0:num_secrets], voiceIds, mp3path,
				 shuffleSecrets=shuffleSecrets, 
				 randVoice=randVoice, 
				 translate_lang=translate_lang, 
				 ssml=ssml, 
				 whisperFreq=whisperFreq, 
				 language=language, 
				 target_lang=target_lang,
				 concatSecretMp3s=concatSecretMp3s,
				 mp3_padding=mp3_padding)

if __name__ == "__main__":
	main(sys.argv[1:])

