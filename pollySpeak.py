#!/usr/bin/env python
'''
Description: wrapper functions for text-to-speech using the Amazon Polly API
Author: Rachel Kalmar (based on examples on the Amazon Polly website)

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

def newSession(profile='default'):
	# Create a client using the credentials and region defined in the [adminuser]
	# section of the AWS credentials file (~/.aws/credentials).
	session = Session(profile_name=profile)
	polly = session.client("polly")
	return polly

def pollySpeech(polly, 
				text='', 
				outputFormat='mp3', 
				voiceId='Joanna', 
				outputFile='pollySpeech',
				speak=False, 
				textType='text',
				verbose=False):
	try:
		# Request speech synthesis
		response = polly.synthesize_speech(Text=text, OutputFormat=outputFormat, VoiceId=voiceId, TextType=textType)
		pprint(response)
		if verbose:
			print ''
	except (BotoCoreError, ClientError) as error:
		# The service returned an error, exit gracefully
		print(error)
		sys.exit(-1)
	# Access the audio stream from the response
	if "AudioStream" in response:
		# Note: Closing the stream is important as the service throttles on the
		# number of parallel connections. Here we are using contextlib.closing to
		# ensure the close method of the stream object will be called automatically
		# at the end of the with statement's scope.
		with closing(response["AudioStream"]) as stream:
			# output = os.path.join(gettempdir(), "speech.mp3")
			output = outputFile + '.' + outputFormat
			try:
				# Open a file for writing the output as a binary stream
				with open(output, "wb") as file:
					file.write(stream.read())
					print('Wrote stream to {}'.format(output))
					if verbose:
						print ''
			except IOError as error:
				# Could not write to file, exit gracefully
				print(error)
				sys.exit(-1)
		if speak:
			playsound(output)
	else:
		# The response didn't contain audio data, exit gracefully
		print("Could not stream audio")
		sys.exit(-1)

def speakSecrets(secrets, voiceIds, mp3path,
				 shuffleSecrets=False, 
				 randVoice=True, 
				 translate_lang=False, 
				 ssml=True, 
				 whisperFreq=0.1, 
				 language='en', 
				 target_lang='en',
				 concatSecretMp3s=True,
				 mp3_padding=1500,
				 verbose=False):
						
	# create a new session
	polly = newSession()

	if ssml:
		textType = 'ssml'
	else:
		textType = 'text'

	for i in range(0, len(secrets)):
		# Choose a new secret 
		if shuffleSecrets:
			idx = random.randint(0,len(secrets))
		else:
			idx = i
		secret = utils.convertUnicode(secrets[idx])
		if verbose:
			print ''
			print 'Processing secret #{}.'.format(idx)
			print ''
		pprint(secret)

		# Skip this secret if it isn't slated for publishing
		if not secret['publish']:
			continue

		# Choose voice
		if randVoice:
			voiceId = random.choice(voiceIds)
			if verbose:
				print ''
				print '{} is speaking this secret'.format(voiceId)
				print ''			
			else:
				print(voiceId)
		else:
			voiceId = voiceIds[0]

		# Decide whether or not to whisper
		if random.random() <= whisperFreq:
			whisperSecret = True
			if verbose:
				print 'This secret is being whispered.'
				print ''			
		else:
			whisperSecret = False

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
			secretText = utils.createSSML(secretText, sentencePause=True, whisper=whisperSecret)
		else:
			secretText = secret['text']

		# Speak and record secret
		pollySpeech(
			polly,
			text=secretText,
			textType=textType,
			voiceId=voiceId,
			outputFile='{}/secret-{}'.format(mp3path,i),
			speak=True,
			verbose=verbose)

	if concatSecretMp3s:
		# Merge all secret mp3s into one merged mp3
		print ''
		print('Now concatenating mp3s...')
		print ''
		concatMp3(mp3path + '/', file_padding=mp3_padding)

# polly = newSession()
# pollySpeech(polly,text='See? Another secret.',voiceId='Amy',speak=True)
