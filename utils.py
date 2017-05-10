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
def addTranslatedSecretsToJSON(csvfile, secrets, fieldname, datapath_translate):
	with open(csvfile) as f:
		reader = csv.reader(f)
		headers = next(reader)
		for idx, row in enumerate(reader):
			print(idx, row[2])
			secrets[idx][fieldname] = row[2]

	with open(datapath_translate, 'w') as f:
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

# Convert unicode for internal processing 
def convertUnicode(data):
	if isinstance(data, string_types):		
		return str(data)
	elif isinstance(data, collections.Mapping):
		if sys.version_info[0] == 2:
			return dict(map(convertUnicode, data.iteritems()))
		else:
			return dict(map(convertUnicode, data.items()))
	elif isinstance(data, collections.Iterable):
		return type(data)(map(convertUnicode, data))
	else:
		return data

