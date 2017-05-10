#!/usr/bin/env python
'''
Take in a directory of mp3s, concatenate all the files into one mp3.

'''

import os
import glob
from pydub import AudioSegment

def concatMp3(mp3dir, file_padding=500):
	os.chdir(mp3dir)
	audio_secrets = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob.glob("*.mp3")]

	merged_secrets = audio_secrets[0][:1]
	silent_buffer = AudioSegment.silent(duration = file_padding)

	for secret in audio_secrets:
		merged_secrets = merged_secrets + secret + silent_buffer

	with open(mp3dir + 'mergedSecrets.mp3', 'wb') as f:
		merged_secrets.export(mp3dir + 'mergedSecrets.mp3', format='mp3')

'''
mp3dir = '/Users/kalmar/Documents/code/secrets/2017-04-26-15-05/'

'''