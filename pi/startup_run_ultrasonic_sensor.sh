#!/bin/sh
sleep 10
amixer cset numid=3 1
amixer sset PCM,0 100%
aplay /home/pi/code/sounds/chime.wav
sudo python /home/pi/code/play_music_list.py &
sudo python /home/pi/code/ultrasonic_vibe.py &
