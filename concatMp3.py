#!/usr/bin/env python
'''
Take in a directory of mp3s, concatenate all the files into one mp3.

'''

import os
import glob
import utils
from random import randint
from pydub import AudioSegment

def concatMp3(mp3dir, file_name='mergedSecrets', file_padding=500):
	os.chdir(mp3dir)
	audio_secrets = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob.glob("secret-*.mp3")]
	
	merged_secrets = audio_secrets[0][:1]

	if file_padding != 'random':
		silent_buffer = AudioSegment.silent(duration = file_padding)
	
	for secret in audio_secrets:
		if file_padding == 'random':
			silent_buffer = AudioSegment.silent(duration = randint(10000,120000))
		merged_secrets = merged_secrets + secret + silent_buffer
		
	print(mp3dir,file_name)
	fname = utils.createUniqueFilename(mp3dir + file_name + '.mp3')
	
	with open(fname, 'wb') as f:
		merged_secrets.export(fname, format='mp3')

'''
mp3dir = '/Users/kalmar/Documents/code/secrets/audio/2017-04-26-15-05/'

'''

