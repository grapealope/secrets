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
import datetime
import re
from pprint import pprint
from six import string_types
from nltk import tokenize
# from google.cloud import translate

# Take in text, create SSML version (synthetic speech markup language) for use 
# with Amazon's Polly API
def createSSML(text, sentencePause=True, whisper=False):
	text = stripInvalidSymbols(text)
	if sentencePause:
		sentences = tokenize.sent_tokenize(text)		
		sentenceBreak = '<break strength="x-strong"/>'
		text = sentenceBreak.join(sentences)
	if whisper:
		text = '<amazon:effect name="whispered">{}</amazon:effect>'.format(text)
	text = '<speak>{}</speak>'.format(text)
	return text

# Strip or replace invalid symbols for SSML
def stripInvalidSymbols(text):
	text = re.sub('<3', '', text)
	text = re.sub('&','and', text)
	text = re.sub('[<>]', '', text)
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
	writeJsonToFile(datapath_translate, secrets, compact=compact)
	
	# with open(datapath_translate, 'w') as f:	
	# 	# Compact: one dict per line	
	# 	if compact:
	# 		# Separate dicts by commas and new lines
	# 		strs = [json.dumps(secretdict, sort_keys=True) for secretdict in secrets]
	# 		s = "[%s]" % ",\n".join(strs)		
	# 		f.write(s)
	# 	else:
	# 		# Each field gets its own line
	# 		json.dump(secrets, f, sort_keys=True, indent=4, separators=(',', ': ')) 

# Take in a csv file with translated secrets, append these to existing JSON for secrets
# Use this version of the function to take in the intended language and whether the secret should be used
def addModifiedTranslatedSecretsToJSON(csvfile, secrets, fieldname, datapath_translate, fixEnglish=False, compact=True):
	with open(csvfile) as f:
		reader = csv.reader(f)
		headers = next(reader)
		for idx, row in enumerate(reader):
			if fixEnglish:
				secrets[idx]['englishString'] = row[1]
				secrets[idx]['text'] = row[1]			
			print(idx, row[2])
			secrets[idx][fieldname] = row[2]
			secrets[idx]['language'] = row[3]
			if row[4] == 'yes':
				secrets[idx]['publish'] = False

	# Write json to file
	writeJsonToFile(datapath_translate, secrets, compact=compact)

	# print('Saving {}...'.format(datapath_translate))
	# with open(datapath_translate, 'w') as f:	
	# 	# Compact: one dict per line	
	# 	if compact:
	# 		# Separate dicts by commas and new lines
	# 		strs = [json.dumps(secretdict, sort_keys=True) for secretdict in secrets]
	# 		s = "[%s]" % ",\n".join(strs)		
	# 		f.write(s)
	# 	else:
	# 		# Each field gets its own line
	# 		json.dump(secrets, f, sort_keys=True, indent=4, separators=(',', ': ')) 

def createSecretsJsonFromCSV(csvfile, datapath, compact=True):
	with open(csvfile) as f:
		reader = csv.reader(f)
		headers = next(reader)
		secrets = []
		for idx, row in enumerate(reader):
			secret = {}
			secret['csv_id'] = row[0]
			secret['createdAt'] = {'$date': None}
			secret['englishString'] = row[1]
			secret['lang'] = 'en'
			secret['owner'] = 'na'
			secret['publish'] = 'true'
			secret['readyToPrintOne'] = 'false'
			secret['readyToPrintTwo'] = 'false'
			secret['source'] = 'remote'
			secret['status'] = 'ok'
			secret['text'] = row[1]	
			print(idx, row[1])
			secrets.append(secret)

	# Write json to file
	writeJsonToFile(datapath, secrets, compact=compact)

def writeJsonToFile(datapath, secrets, compact=True):
	# Write json to file
	print('Saving {}...'.format(datapath))
	with open(datapath, 'w') as f:	
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
			if not os.path.isfile(new_name):
				unique_fname = True
			else:
				idx+=1
		return new_name
	elif os.path.isdir(fname):
		unique_fname = False
		idx = 0
		f_base = fname
		while unique_fname is False:
			new_name = '{}-{}'.format(f_base, idx)
			if not os.path.isdir(new_name):
				unique_fname = True
			else:
				idx+=1
		return new_name
	else:
		return fname

# Creates timestamped directory within a base directory
def createTimestampedDir(basepath):
	now = datetime.datetime.now()
	ts_path = '{}{}'.format(basepath,now.strftime('%Y-%m-%d-%H-%M'))
	ts_path = createUniqueFilename(ts_path)
	os.mkdir(ts_path)
	return ts_path


# Flatten a nested list
# source: https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)