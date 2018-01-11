#!/usr/bin/python

#Libraries
import RPi.GPIO as GPIO
import time
import pygame
from time import sleep
import random

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
LED_1 = 23
MOTOR_GREEN = 17
MOTOR_WHITE = 27

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(MOTOR_GREEN, GPIO.OUT)
GPIO.setup(MOTOR_WHITE, GPIO.OUT)

# Initialize pygame
pygame.init()
pygame.mixer.init()
sound_coin = pygame.mixer.Sound("/home/pi/code/sounds/coin.wav")
sound_burp = pygame.mixer.Sound("/home/pi/code/sounds/burp.wav")
sound_hans = pygame.mixer.Sound("/home/pi/code/sounds/danke-hans.wav")
sound_vicki = pygame.mixer.Sound("/home/pi/code/sounds/danke-vicki.wav")
sound_marlene = pygame.mixer.Sound("/home/pi/code/sounds/danke-marlene.wav")

# Initialize outputs
GPIO.output(LED_1, GPIO.LOW)
GPIO.output(MOTOR_GREEN, GPIO.LOW)
GPIO.output(MOTOR_WHITE, GPIO.LOW)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
	    if (dist < 10):
		die_roll = random.randint(0,100)
		print('die roll: {}'.format(die_roll))
		if die_roll < 10:
			print("Playing sound now: Vicki")
			sound_vicki.play()
		elif (die_roll >= 10) and (die_roll < 20):
                        print("Playing sound now: Hans")
                        sound_hans.play()
		elif (die_roll >= 20) and (die_roll < 30):
                        print("Playing sound now: Marlene")
                        sound_marlene.play()
		elif (die_roll >= 95) and (die_roll < 100):
                        print("Playing sound now: coins")
                        sound_coin.play()
		elif die_roll == 100:
			print("Playing sound now: jelly baby")
			sound_burp.play()
		print("Turning on LED")
		GPIO.output(LED_1, GPIO.HIGH)
		print("Turning on vibe motors")
		GPIO.output(MOTOR_GREEN, GPIO.HIGH)
		GPIO.output(MOTOR_WHITE, GPIO.HIGH)
		sleep(2)
		if die_roll < 10:
			sound_vicki.stop()
		elif (die_roll >= 10) and (die_roll < 20):
                        sound_hans.stop()
		elif (die_roll >= 20) and (die_roll < 30):
                        sound_marlene.stop()
		elif (die_roll >= 95) and (die_roll < 100):
                        sound_coin.stop()
		elif die_roll == 100:
			sound_burp.stop()
		print("Turning off LED")
		GPIO.output(LED_1, GPIO.LOW)
		print("Turning off vibe motors")
		GPIO.output(MOTOR_GREEN, GPIO.LOW)
		GPIO.output(MOTOR_WHITE, GPIO.LOW)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")

    finally:
	print("Cleaning up")
	GPIO.output(MOTOR_GREEN, GPIO.LOW)
	GPIO.output(MOTOR_WHITE, GPIO.LOW)
	GPIO.output(LED_1, GPIO.LOW)
#        GPIO.cleanup()
