# avian-rpi

Runs `sample.mp3` on a defined schedule.

Current sample.mp3 is `https://macaulaylibrary.org/asset/229691`.

## Pre-Installation

Use Balena Etcher to install the latest Raspbian OS. You should use a Pi Model 3 or later so you have WiFi to make it easier to update the device.

Run `sudo rpi-update` to update the pi firmware.

Set `hdmi_force_hotplug=1` in `/boot/config.txt`.

## Installation

Once this is run, it will run `configure.sh` every 5 minutes if there is an internet connection.

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
