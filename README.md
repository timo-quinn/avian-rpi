# avian-rpi

Runs `sample.mp3` on a defined schedule.

Current sample.mp3 is `https://macaulaylibrary.org/asset/229691`.

## Pre-Installation

Use Balena Etcher to install the latest Raspbian OS. You should use a Pi Model 3 or later so you have WiFi to make it easier to update the device.

Configure the pi with default configuration. Join it to a WiFi network that you can disconnect/reconnect easily with the Pi (such as a mobile phone hotspot).

Run `sudo rpi-update` to update the pi firmware.

Set `hdmi_force_hotplug=1` in `/boot/config.txt`.

## Installation

Once this is run, it will run `configure.sh` every 2 minutes. Every 2 minutes:

1. if internet is connected, it will pull down the latest version of this repo.
2. if it hasn't been installed yet, then it will run the installation part of the script.
3. it will call the play_sample.py script. If the last time it ran is greater than the config in `config.json`, then it will play the sample audio.

Open a terminal and run:

``` bash
cd /home/pi/Desktop/
wget https://raw.githubusercontent.com/timo-quinn/avian-rpi/master/configure.sh
sh configure.sh
```

## Reinstallation

You shouldn't need to do this, but if you need to purge the current setup and start again:

Open a terminal and run:

``` bash
cd /home/pi/Desktop/
rm -rf avian-rpi/
rm -f is_installed
rm -f configure.sh
wget https://raw.githubusercontent.com/timo-quinn/avian-rpi/master/configure.sh
sh configure.sh
```
