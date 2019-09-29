#!/bin/sh
cd /home/pi/Desktop

# test if the internet is connected
is_online=false
is_already_installed=false

# testing if there is internet
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
    echo "is online"
    is_online=true
fi

# test if already installed
FILE=/home/pi/Desktop/is_installed
if [ -f "$FILE" ]; then
    echo "is installed"
    is_already_installed=true
fi

# if not online, return an error and stop
if [ "$is_online" = false ] ; then
    exit 1
fi

# if not already installed, then get the repo and run the install script
if [ "$is_already_installed" = false ] ; then
    git config --global user.email "none"
    git config --global user.name "none"

    pip3 install pygame # pygame is used for audio playback
    git clone https://github.com/timo-quinn/avian-rpi.git
    cd /home/pi/Desktop/avian-rpi/
    # make all the files executable
    chmod -R +x .
    # purge crontab
    crontab -r
    # set up the cron job to run this configure script every 5 minutes
    (crontab -l 2>/dev/null; echo "*/5 * * * * sh /home/pi/Desktop/avian-rpi/configure.sh") | crontab -

    sudo /bin/cp -f rc.local /etc/rc.local

    # two beeps to mark that it's configured
    python3 play_beep.py
    python3 play_beep.py

    # create the is_installed folder to make sure this only runs once
    cd /home/pi/Desktop/
    touch is_installed
else # pull down the latest configuration
    cd /home/pi/Desktop/avian-rpi

    git stash # stash changes to make sure they don't interfere with the updates
    git pull # pull the latest master branch
    python3 play_beep.py # one beep to mark it's been updated
fi

exit 0
