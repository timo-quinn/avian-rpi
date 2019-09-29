import sys
import pygame
from datetime import datetime
import time
import logging
import json

repo_dir = '/home/pi/Desktop/avian-rpi/'
desktop_dir = '/home/pi/Desktop/'
# repo_dir = ''
# desktop_dir = ''
log_file_name = desktop_dir + 'play_sample.log'
print(repo_dir)
print(desktop_dir)
print(log_file_name)

logging.basicConfig(filename=log_file_name, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def write_state(state_to_write):
  to_write = state_to_write
  to_write["last_run_time"] = datetime.now().timestamp()
  with open(desktop_dir + 'state.json', 'w') as outfile:
    json.dump(to_write, outfile, indent=4, separators=(',', ': '))


with open(repo_dir + 'config.json') as config_file:
  config = json.load(config_file)


try:
  with open(desktop_dir + 'state.json') as state_file:
    run_state = json.load(state_file)
except:
  with open(repo_dir + 'default_state.json') as state_file:
    run_state = json.load(state_file)


frequency = config['frequency']
last_run_timestamp = run_state['last_run_time']
current_time = datetime.now()

if last_run_timestamp != "":
  last_run_time = datetime.fromtimestamp(last_run_timestamp)
else:
  last_run_time = datetime.now()
  write_state(run_state)

print('current time: ', current_time)
print('last run time: ', last_run_time)
minutes_difference = (current_time - last_run_time).total_seconds() / 60.0
print('minutes difference: ', minutes_difference)
print('frequency: ', frequency)


# we only execute the script if the last run time is greater than the configured frequency
if minutes_difference > frequency:
  logging.info("starting sample script")
  print("starting sample script")
  pygame.mixer.init()

  logging.info("playing sample")
  print("playing sample")
  pygame.mixer.music.load(repo_dir + 'sample.mp3')
  pygame.mixer.music.play()

  write_state(run_state)

  while pygame.mixer.music.get_busy() == True:
    logging.debug("still playing")
    print("still playing")
    time.sleep(20)
    continue

  logging.info("sample script completed")
  print("sample script completed")
