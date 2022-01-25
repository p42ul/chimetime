# Chime Time

## Steps to get it working on a Raspberry Pi

This guide assumes that you've installed Raspbian OS. At the time of writing, I started with Raspbian Lite, Release date: October 30th 2021.
Please also make sure Python 3.x is installed.

```
cd ~
# Apt stuff.
sudo apt update
sudo apt upgrade
sudo apt install git python3-gpiozero python3-pip 

# Install Python packages.
sudo pip3 install --upgrade setuptools adafruit-circuitpython-mcp230xx adafruit-python-shell watchdog gunicorn

# Install and test CircuitPython Blinka.
# From https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi.
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
cat << EOF > blinkatest.py
import board
import digitalio
import busio
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok!")
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")
EOF
python3 blinkatest.py

# Use our default config file
cp default_config.json config.json

# Create and start the Chime Time service.
sudo cp chimetime.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable chimetime.service
```



