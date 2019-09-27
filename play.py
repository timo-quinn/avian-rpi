import sys
import pygame
import time

print("starting script")
pygame.mixer.init()

def play_beep():
  print("playing beep")
  pygame.mixer.music.load('beep2.mp3')
  pygame.mixer.music.play()

def play_sample():
  print("playing sample")
  pygame.mixer.music.load('sample.mp3')
  pygame.mixer.music.play()

play_beep()

while pygame.mixer.music.get_busy() == True:
  print("still playing")
  time.sleep(5)
  continue

print("script completed")