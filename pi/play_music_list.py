#!/usr/bin/python

# Libraries
import os
import glob
import time
import pygame

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Create a function to play the next song
def play_next_song():
	global _mp3_files
	_mp3_files = _mp3_files[1:] + [_mp3_files[0]]
	print('Now playing: {}'.format(_mp3_files[0]))
	pygame.mixer.music.load(_mp3_files[0])
	pygame.mixer.music.play()

# Change to the directory with the mp3 files
mp3_dir = '/media/usb1/secrets/'

try:
	os.chdir(mp3_dir)

	# Get a list of the mp3s in this directory
	_mp3_files = sorted([mp3_file for mp3_file in glob.glob("*.mp3")])

	# Set up our music player
	SONG_END = pygame.USEREVENT + 1

	pygame.mixer.music.set_endevent(SONG_END)
	pygame.mixer.music.load(_mp3_files[0])
	pygame.mixer.music.play()

	try:
		while True:
			for event in pygame.event.get():
				if event.type == SONG_END:
					play_next_song()
	except KeyboardInterrupt:
		print('Stoppping the music!')

except:
	print('{} does not exist or does not contain mp3s; please check and try again'.format(mp3_dir))
