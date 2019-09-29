import sys
import pygame
import time
import logging

logging.basicConfig(filename='/home/pi/Desktop/sample.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("starting sample script")
pygame.mixer.init()

def play_sample():
  logging.info("playing sample")
  pygame.mixer.music.load('/home/pi/Desktop/avian-rpi/sample.mp3')
  pygame.mixer.music.play()

play_sample()
time.sleep(1)

while pygame.mixer.music.get_busy() == True:
  logging.debug("still playing")
  time.sleep(20)
  continue

logging.info("sample script completed")
