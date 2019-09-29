import sys
import pygame
import time
import logging

logging.basicConfig(filename='/home/pi/Desktop/beep.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("starting beep script")
pygame.mixer.init()

logging.info("playing beep")
pygame.mixer.music.load('/home/pi/Desktop/avian-rpi/beep2.mp3')
pygame.mixer.music.play()

time.sleep(1)

logging.info("beep script completed")
