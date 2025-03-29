#!/usr/bin/env python

from time import sleep, time
import os
import logging

import click
import RPi.GPIO as GPIO
from vlc_player import VLC

GPIO.setmode(GPIO.BCM)
PIR_PIN = 25
BTN_PIN = 28

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BTN_PIN, GPIO.IN)

PLAY_TIME = 60*5
TIMEOUT = 15

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("__name__")


def motion_detected(player: VLC, playtime: int = PLAY_TIME):
    logger.info("Motion detected")
    player.play()
    sleep(PLAY_TIME)
    player.pause()


def btn_press_detected(pin: int, player: VLC, long_press: int = 10):
    global buttonStatus
    start_time = time()
    logger.info("Btn pressed")
    while GPIO.input(pin) == 0 and (time() - start_time) < TIMEOUT:
        pass

    buttonTime = time() - start_time    # How long was the button down?

    logger.info("Btn released")
    logger.info(f"Button time: {buttonTime}")

    if buttonTime >= .1:    # Ignore noise
        player.next()       # 1= brief push
    elif buttonTime >= long_press:
        os.system('shutdown -s')


@click.command()
@click.option('--path', default="/home/sepp/media",
              help="Path to the media directory")
@click.option('--timeout', default=10, help='System shutdown after x seconds')
@click.option('--playtime', default=PLAY_TIME, help='Play for x seconds')
def run(path, timeout, playtime):
    player = VLC()
    player.addPlaylist(path=path)
    logger.info(
        "Media Player started: \n\t{timeout}\n\t{playtime}\n\t Path: {path}")
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING,
                          callback=lambda channel: motion_detected(player,
                                                                   playtime=playtime))
    GPIO.add_event_detect(BTN_PIN, GPIO.PUD_DOWN, callback=lambda channel:
                          btn_press_detected(BTN_PIN, player, timeout))
    while True:
        sleep(1)


if __name__ == "__main__":
    run()
