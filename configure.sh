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
    pip3 install pygame # pygame is used for audio playback
    git clone https://github.com/timo-quinn/avian-rpi.git
    cd /home/pi/Desktop/avian-rpi/

    # set up the cron job to run this configure script every 5 minutes
    grep 'pi sh /home/pi/Desktop/avian-rpi/configure.sh' /etc/crontab || echo '*/5 *  *  *  * pi python3 /home/pi/Desktop/avian-rpi/configure.sh' >> /etc/crontab
    
    cd /home/pi/Desktop/
    # create the is_installed folder to make sure this only runs once
    touch is_installed
else
    cd /home/pi/Desktop/avian-rpi
    # fetch the latest master
    git pull
fi

exit 0
