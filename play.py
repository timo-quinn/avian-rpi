import sys
import pygame
import time

print("starting playback")
pygame.mixer.init()
pygame.mixer.music.load('beep2.mp3')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy() == True:
  print("still playing")
  time.sleep(5)
  continue
