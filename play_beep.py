import sys
import pygame
import time
import logging

logging.basicConfig(filename='beep.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("starting beep script")
pygame.mixer.init()

def play_beep():
  logging.info("playing beep")
  pygame.mixer.music.load('beep2.mp3')
  pygame.mixer.music.play()

play_beep()
time.sleep(1)

while pygame.mixer.music.get_busy() == True:
  logging.debug("still playing")
  time.sleep(5)
  continue

logging.info("beep script completed")
