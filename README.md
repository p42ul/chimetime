# Chime Time

## Steps to get it working

This guide assumes that you've installed Raspbian OS. At the time of writing, I started with Raspbian Lite, Release date: October 30th 2021.
Please also make sure Python 3.x is installed.

`sudo raspi-config`

`sudo apt update`

```
cd ~
sudo raspi-config
sudo apt update
sudo apt upgrade
sudo apt install git python3-gpiozero python3-pip
sudo pip3 install --upgrade setuptools
: (This part is taken from https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
cat << EOF > blinkatest.py
import board
import digitalio
import busio

print("Hello blinka!")

# Try to great a Digital input
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok!")

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

# Try to create an SPI device
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")

print("done!")
EOF
python3 blinkatest.py
sudo pip3 install adafruit-circuitpython-mcp230xx

# Create and start the Chime Time service.
sudo cp chimetime.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable chimetime.service
```



