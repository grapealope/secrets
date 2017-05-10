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

def newSession(profile='default'):
	# Create a client using the credentials and region defined in the [adminuser]
	# section of the AWS credentials file (~/.aws/credentials).
	session = Session(profile_name=profile)
	polly = session.client("polly")
	return polly

def pollySpeech(polly, text='', outputFormat='mp3', voiceId='Joanna', outputFile='pollySpeech',speak=False, textType='text'):
	try:
		# Request speech synthesis
		response = polly.synthesize_speech(Text=text, OutputFormat=outputFormat, VoiceId=voiceId, TextType=textType)
		pprint(response)
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


# polly = newSession()
# pollySpeech(polly,text='See? Another secret.',voiceId='Amy',speak=True)
