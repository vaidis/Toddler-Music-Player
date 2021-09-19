#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from mpd import MPDClient
from os import listdir
from os.path import isfile, join


#
# Settings
#
DIR_MUSIC = "/var/lib/mpd/music"
DIR_PLAYLIST = "/var/lib/mpd/playlists/main.m3u"

PLAY_BUTTONS = [21, 20,16, 12, 7, 23, 18, 24, 25, 8 ]
PLAY_LEDS = [9, 10, 22, 27, 17, 26, 19, 13, 6, 5 ]
STOP_BUTTON = 2
STOP_LED = 11


#
# Create the playlist
#
FILES = [f for f in listdir(DIR_MUSIC) if isfile(join(DIR_MUSIC, f))]
FILES.sort()

with open(DIR_PLAYLIST, 'w', encoding='utf-8') as p:
    for f in FILES:
        print(f, file=p)


#
# Initialize MPD
#
mpc = MPDClient()
mpc.connect("localhost", 6600)

mpc.clear()         # clear the old playlist
mpc.update()        # find new, remove or update files
mpc.rescan()        # rescans unmodified files
mpc.load("main")    # load playlist main.m3u
mpc.single(1)       # stop after current song
mpc.repeat(0)       # do not repeat
mpc.setvol(75)      # volume max
mpc.stop()


#
# Initialize GPIO pins
#
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set input pins for buttons
def setup_all_buttons():
    for PLAY_BUTTON in PLAY_BUTTONS:
        GPIO.setup(PLAY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set output pins for leds
def setup_all_leds():
    for PLAY_LED in PLAY_LEDS:
        GPIO.setup(PLAY_LED, GPIO.OUT)
    GPIO.setup(STOP_LED, GPIO.OUT)

# turn off leds
def reset_play_leds():
    for PLAY_LED in PLAY_LEDS:
        GPIO.output(PLAY_LED, GPIO.LOW)
    GPIO.output(STOP_LED, GPIO.LOW)

# test leds
def test_leds():
    for LED in PLAY_LEDS:
        GPIO.output(LED, GPIO.HIGH)
        time.sleep(0.1)

    for LED in PLAY_LEDS:
        GPIO.output(LED, GPIO.LOW)
        time.sleep(0.1)

    GPIO.output(STOP_LED, GPIO.HIGH)

setup_all_buttons()
setup_all_leds()
reset_play_leds()
test_leds()


#
# Play / Stop songs and handle leds
#
def play(song):
    pressed = True
    ping = song - 1
    mpc.play(song)
    reset_play_leds()
    GPIO.output(PLAY_LEDS[song - 1], GPIO.HIGH)
    GPIO.output(STOP_LED, GPIO.LOW)


def stop():
    mpc.stop()
    reset_play_leds()
    GPIO.output(STOP_LED, GPIO.HIGH)


#
# Main
#
if __name__ == '__main__':
    pressed = False

    while True:

        # enable stop led if not play
        status = mpc.status()
        if status['state'] != "play":
            reset_play_leds()
            GPIO.output(STOP_LED, GPIO.HIGH)

        # watch for pressed button
        if not GPIO.input(PLAY_BUTTONS[0]):
            if not pressed:
                play(1)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[1]):
            if not pressed:
                play(2)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[2]):
            if not pressed:
                play(3)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[3]):
            if not pressed:
                play(4)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[4]):
            if not pressed:
                play(5)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[5]):
            if not pressed:
                play(6)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[6]):
            if not pressed:
                play(7)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[7]):
            if not pressed:
                play(8)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[8]):
            if not pressed:
                play(9)
        else:
            pressed = False

        if not GPIO.input(PLAY_BUTTONS[9]):
            if not pressed:
                play(10)
        else:
            pressed = False

        if not GPIO.input(STOP_BUTTON):
            if not pressed:
                stop()
        else:
            pressed = False

        time.sleep(0.2)  # ignore fast button press
