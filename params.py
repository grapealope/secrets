#!/usr/bin/env python
'''
Description: these are the default parameters to use for processing secrets data
Author: Rachel Kalmar

'''

# Defaults 

datapath = '/Users/kalmar/Documents/code/secrets/secrets_data/secrets_edit_edit.json'
mp3path_base = '/Users/kalmar/Documents/code/secrets/audio/'
shuffleSecrets = False
language = 'en'
translate = False
translate_to = 'it'
speak = True
ssml = True
mp3_padding = 500

if ssml:
	textType = 'ssml'
else:
	textType = 'text'