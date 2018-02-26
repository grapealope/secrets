#!/usr/bin/env python
'''
Take in a directory of mp3s, concatenate all the files into one mp3.

'''

import os
import glob
import utils
from random import randint, choice
from pydub import AudioSegment
from utils import flatten

def concatMp3(mp3dir, file_name='mergedSecrets', file_padding=500, random_min=1000, random_max=4000, 
			  range_start=None, range_stop=None, verbose=False, attenuation_list=None):
	
	os.chdir(mp3dir)
	
	if (range_start is not None) and (range_stop is not None):
		fnames = flatten([glob.glob("secret-{}.mp3".format(i)) for i in range(range_start, range_stop+1)])
	else:
		fnames = glob.glob("secret-*.mp3")
		
	if verbose:
		print("Loading {} files...".format(len(fnames)))
		
	audio_secrets = [AudioSegment.from_mp3(mp3_file) for mp3_file in fnames]
	
	try:
		merged_secrets = audio_secrets[0][:1]
	except:
		print("Error: {} mp3 files in {}; aborting.".format(len(audio_secrets), mp3dir))
		
	if file_padding != 'random':
		silent_buffer = AudioSegment.silent(duration = file_padding)
	
	attenuations_used = []
	file_padding_used = []
	for secret in audio_secrets:
		if file_padding == 'random':
			silent_buffer_length = randint(random_min, random_max)
			silent_buffer = AudioSegment.silent(duration = silent_buffer_length)
			file_padding_used.append(silent_buffer_length)
		else:
			file_padding_used.append(file_padding)
		if attenuation_list:
			attenuation = choice(attenuation_list)
			attenuations_used.append(attenuation)
			secret = secret.apply_gain(-attenuation)
		else:
			attenuations_used.append(0)
		merged_secrets = merged_secrets + secret + silent_buffer
		
	print(mp3dir,file_name)
	fname = utils.createUniqueFilename(mp3dir + file_name + '.mp3')
	
	with open(fname, 'wb') as f:
		merged_secrets.export(fname, format='mp3')
		
	return(attenuations_used, file_padding_used)

'''
mp3dir = '/Users/kalmar/Documents/code/secrets/audio/2017-04-26-15-05/'

'''

'''
file_name = 'mergedSecrets_dB'
audio_secrets_new = [audio_secrets[1] for i in range(10)]
file_padding = 500
silent_buffer = AudioSegment.silent(duration = file_padding)

merged_secrets = audio_secrets_new[0][:1]
for i, secret in enumerate(audio_secrets_new):
	secret = secret.apply_gain(-i)
	merged_secrets = merged_secrets + secret + silent_buffer

merged_secrets = audio_secrets_new[0][:1]
for i, secret in enumerate(audio_secrets_new[0:5]):
	secret = secret.apply_gain(-i*2.5)
	merged_secrets = merged_secrets + secret + silent_buffer

fname = utils.createUniqueFilename(mp3dir + file_name + '.mp3')
with open(fname, 'wb') as f:
	merged_secrets.export(fname, format='mp3')
'''
