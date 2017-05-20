#!/usr/bin/env python
'''
Description: these are the default parameters to use for processing secrets data
Author: Rachel Kalmar

'''

# ------------------------------------ #
# Set defaults for parameters to be used in secretReaderPollyVoices

datapath_base = '/Users/kalmar/Documents/code/secrets/secrets_data/'  # Where the secrets data is kept
mp3path_base = '/Users/kalmar/Documents/code/secrets/audio/'		  # Where to store the audio output
shuffleSecrets = False		# Shuffle the order of the secrets?
speak = True				# Speak secrets?
ssml = True					# Use speech synthesis markup language?
mp3_padding = 1500			# Buffer between mp3 files, for concatenated mp3

# ------------------------------------ #
# Set language and translation params

translate_lang = False

#language = 'en'
language = 'it'
#language = 'de'

target_lang = 'it'
#target_lang = 'de'

if language=='en':
	# voiceIds = ['Joanna', 'Salli', 'Kimberly', 'Kendra', 'Amy', 'Ivy', 'Justin', 'Joey', 'Brian']
	voiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']		
elif language=='it':
	voiceIds = ['Carla', 'Giorgio']
elif language=='de':
	voiceIds = ['Marlene', 'Hans']

voice = voiceIds[0]

# ------------------------------------ #
# Set params based on options chosen above

if language == 'en':
	datapath = datapath_base + 'secrets_edit_edit.json'
elif language == 'it':
	datapath = datapath_base + 'secrets_edit_italian_temp.json'
elif language == 'de':
	datapath = datapath_base + 'secrets_edit_german.json'

if ssml:
	textType = 'ssml'
else:
	textType = 'text'