#!/usr/bin/env python
'''
Description: a collection of utility functions for wrangling data from secrets.
Author: Rachel Kalmar

'''

import os, sys
import json
import csv
import collections
import random
from pprint import pprint
from six import string_types
from nltk import tokenize
from google.cloud import translate

# Take in text, create SSML version (synthetic speech markup language) for use 
# with Amazon's Polly API
def createSSML(text, sentencePause=True, whisper=False):
	if sentencePause:
		sentences = tokenize.sent_tokenize(text)		
		sentenceBreak = '<break strength="x-strong"/>'
		text = sentenceBreak.join(sentences)
	if whisper:
		text = '<amazon:effect name="whispered">{}</amazon:effect>'.format(text)
	text = '<speak>{}</speak>'.format(text)
	return text

# Take in a csv file with translated secrets, append these to existing JSON for secrets
def addTranslatedSecretsToJSON(csvfile, secrets, fieldname, datapath_translate, compact=True):
	with open(csvfile) as f:
		reader = csv.reader(f)
		headers = next(reader)
		for idx, row in enumerate(reader):
			print(idx, row[2])
			secrets[idx][fieldname] = row[2]

	# Write json to file
	with open(datapath_translate, 'w') as f:	
		# Compact: one dict per line	
		if compact:
			# Separate dicts by commas and new lines
			strs = [json.dumps(secretdict, sort_keys=True) for secretdict in secrets]
			s = "[%s]" % ",\n".join(strs)		
			f.write(s)
		else:
			# Each field gets its own line
			json.dump(secrets, f, sort_keys=True, indent=4, separators=(',', ': ')) 

# Take in secrets, translate to specified language and export to a csv
def translateToCSV(secrets, csvfile, target_lang):
	translate_client = translate.Client()
	with open(csvfile, "wb+") as file:
		csv_file = csv.writer(file)
		if target_lang == 'de':
			csv_file.writerow(['index','secret (english)', 'secret (german)'])
		elif target_lang == 'it':
			csv_file.writerow(['index','secret (english)', 'secret (italian)'])
		for i in range(len(secrets)):
			idx = i
			secret = secrets[idx]
			secretText = secret['text']
			translation = translate_client.translate(
								secretText,
								target_language=target_lang,
								format_='text')
			secretText = translation['translatedText']
			print(i, secret['text'], secretText)
			csv_file.writerow([idx, 
						secret['text'], 
						secretText.encode("utf-8")])

def convertUnicode(input):
	if isinstance(input, dict):
		return {convertUnicode(key): convertUnicode(value)
				for key, value in input.iteritems()}
	elif isinstance(input, list):
		return [convertUnicode(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	else:
		return input

# Take in a filename (including path), increment index at end if file already exists
def createUniqueFilename(fname):
	if os.path.isfile(fname):
		unique_fname = False		
		idx = 0
		f_base = os.path.splitext(fname)[0]
		f_ext = os.path.splitext(fname)[1]
		while unique_fname is False:
			new_name = '{}-{}{}'.format(f_base, idx, f_ext)
			print(idx, new_name)
			if not os.path.isfile(new_name):
				unique_fname = True
			else:
				idx+=1
		return new_name
	else:
		return fname