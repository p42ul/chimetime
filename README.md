# Chime Time

## Steps to get it working

This guide assumes that you've installed Raspbian OS. At the time of writing, I started with Raspbian Lite, Release date: October 30th 2021.
Please also make sure Python 3.x is installed (it was installed by default with the version of Raspbian I used).

```
sudo raspi-config
sudo apt update
sudo apt upgrade
sudo apt install git python3-gpiozero python3-pip
sudo pip3 install --upgrade setuptools
: (This part is taken from https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
```
