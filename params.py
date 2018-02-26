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
whisperFreq = 0.15			# What percentage of the secrets should be whispered?
mp3_padding = 1500			# Buffer between mp3 files, for concatenated mp3
concatSecretMp3s = True     # Concatenate the individual mp3 files in a group

datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_edit_rk.json'

# ------------------------------------ #
# Set language and translation params

translate_lang = False

language = 'en'
# language = 'it'
# language = 'de'

target_lang = 'en'
# target_lang = 'it'
# target_lang = 'de'

englishVoiceIds = ['Joanna', 'Kendra', 'Amy', 'Joey', 'Brian']	
italianVoiceIds = ['Carla', 'Giorgio']
germanVoiceIds = ['Vicki', 'Marlene', 'Hans']

if language=='en':
	# voiceIds = ['Joanna', 'Salli', 'Kimberly', 'Kendra', 'Amy', 'Ivy', 'Justin', 'Joey', 'Brian']
	voiceIds = englishVoiceIds
elif language=='it':
	voiceIds = italianVoiceIds
elif language=='de':
	voiceIds = germanVoiceIds

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