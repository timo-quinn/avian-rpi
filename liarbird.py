import configparser
import logging
import os
import time
import json
import requests
import pygame
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys

config = configparser.ConfigParser()
config.read('config.ini')

auth_key = config['general'].get('auth_key')
device_uid = config['general'].get('device_uid')
force_playback_only = config['general'].getboolean('force_playback_only')
interval = config['device'].getint('interval')
sample_file = config['device'].get('sampleFile')

logging.basicConfig(
    handlers=[RotatingFileHandler(filename='liarbird.log', mode='a', maxBytes=10000000, backupCount=10)],
    level=10,
    format='%(asctime)s %(levelname)-6s %(lineno)d %(name)-6s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logging.debug(auth_key)
logging.debug(device_uid)
logging.debug(interval)
logging.debug(sample_file)

if __name__ == '__main__':
  internet_connected = True
  try:
    logging.info('testing internet connectivity')
    request = requests.get("http://google.com", timeout=5)
  except (requests.ConnectionError, requests.Timeout):
    internet_connected = False

  try:
    if internet_connected and not force_playback_only:
      logging.info("internet connection found. running in configuration mode")

      if not device_uid:
        logging.info('no device identifier set - registering device')
        response = requests.post("https://us-central1-liarbird-1df1e.cloudfunctions.net/registerDevice", data={ "authKey": auth_key })
        
        if response.status_code != 200:
          logging.error(response)

        else:
          logging.debug(response.text)
          json_response = json.loads(response.text)
          config.set('general', 'device_uid', json_response['uid'])
          device_uid = json_response['uid']

          logging.info('updating config.ini')
          config.write(open('config.ini', 'w'))

      if device_uid:
        logging.info('fetching config')
        response = requests.post("https://us-central1-liarbird-1df1e.cloudfunctions.net/getConfiguration", data={ "authKey": auth_key, "uid": device_uid })

        if response.status_code != 200:
          # failed request
          logging.error(response)

        else:
          logging.info('config retrieved from server')
          logging.debug(response.text)
          response_data = json.loads(response.text)

          if 'playbackFrequency' in response_data:
            config.set('device', 'interval', response_data['playbackFrequency'])
            config.write(open('config.ini', 'w'))
          if 'sampleFile' in response_data:
            config.set('device', 'sampleFile', response_data['sampleFile'])
            config.write(open('config.ini', 'w'))
          if 'sampleUri' in response_data:
            logging.info('fetching sample')
            response = requests.get(response_data["sampleUri"])

            config.write(open('config.ini', 'w'))

            logging.info('writing sample to disk')
            open(response_data["sampleFile"], 'wb').write(response.content)

    else:
      logging.info("NO internet connection found. running in playback mode")

      if not sample_file:
        logging.error("missing sample file!")
      elif not interval:
        logging.error("missing interval!")
      else:
        logging.info("running as normal")
        pygame.mixer.init()
        while True:
          logging.info("starting playback of sample_file")
          pygame.mixer.music.load(sample_file)
          pygame.mixer.music.play()
          
          time.sleep(interval * 60)

  except (IOError, SystemExit):
    logging.error('IOError or SystemExit')
    raise
  except KeyboardInterrupt:
    logging.error('Ctrl+C Interrupt')
    print("Crtl+C Pressed. Shutting down.")
