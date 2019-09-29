import sys
import pygame
from datetime import datetime
import time
import logging
import json

logging.basicConfig(filename='/home/pi/Desktop/play_sample.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

with open('/home/pi/Desktop/avian-rpi/config.json') as config_file:
  config = json.load(config_file)


try:
  with open('/home/pi/Desktop/state.json') as state_file:
    run_state = json.load(state_file)
except:
  with open('/home/pi/Desktop/avian-rpi/default_state.json') as state_file:
    run_state = json.load(state_file)


frequency = config['frequency']
last_run_timestamp = run_state['last_run_time']
current_time = datetime.now()

if last_run_timestamp != "":
  last_run_time = datetime.fromisoformat(last_run_timestamp)
else:
  last_run_time = datetime.now()

minutes_difference = (current_time - last_run_time).seconds / 60.0

def write_state(state_to_write):
  to_write = state_to_write
  to_write["last_run_time"] = datetime.now().__str__()
  with open('/home/pi/Desktop/state.json', 'w') as outfile:
    json.dump(to_write, outfile, indent=4, separators=(',', ': '))

# we only execute the script if the last run time is greater than the configured frequency
if minutes_difference > frequency:
  logging.info("starting sample script")
  pygame.mixer.init()

  logging.info("playing sample")
  pygame.mixer.music.load('/home/pi/Desktop/avian-rpi/sample.mp3')
  pygame.mixer.music.play()

  write_state(run_state)

  while pygame.mixer.music.get_busy() == True:
    logging.debug("still playing")
    time.sleep(20)
    continue

  logging.info("sample script completed")
