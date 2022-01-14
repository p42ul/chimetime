"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import CTButton
from ct_mappings import ct1_led_map, ct1_solenoid_map
from ct_mux import CTMux
from ct_time import CTTime

import logging
import signal
import sys
from time import sleep

import board
import busio
from gpiozero import Button

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
CT_BUTTON_GPIO_PIN = 21
POLLING_INTERVAL = 0.1
SOLENOID_ON_TIME = 0.1
INTERDIGIT_DELAY = 0.5

MAJOR_ARP = [1, 3, 5, 8]

def button_press_handler(solenoid_mux, led_mux, clock):
    logging.debug('CT button press detected.')
    digits = clock.get_time_digits()
    play_arp(solenoid_mux)
    sleep(INTERDIGIT_DELAY * 2)
    for d in digits:
        solenoid_mux.on(d)
        led_mux.on(d)
        sleep(SOLENOID_ON_TIME)
        solenoid_mux.off(d)
        led_mux.off(d)
        sleep(INTERDIGIT_DELAY)

def play_arp(solenoid_mux):
    for d in MAJOR_ARP:
        solenoid_mux.on(d)
        sleep(SOLENOID_ON_TIME)
        solenoid_mux.off(d)
        sleep(INTERDIGIT_DELAY / 3)

def init_i2c():
    logging.info('Initializing I2C...')
    i2c = busio.I2C(board.SCL, board.SDA)
    logging.info('I2C initialized.')
    return i2c


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting Chime Time...')
    i2c = init_i2c()
    solenoid_mux = CTMux(i2c, SOLENOID_MUX_ADDR, ct1_solenoid_map)
    led_mux = CTMux(i2c, LED_MUX_ADDR, ct1_led_map)
    button = CTButton(CT_BUTTON_GPIO_PIN)
    clock = CTTime()
    def all_off():
        logging.info('Turning off all mux outputs.')
        for m in (solenoid_mux, led_mux):
            m.all_off()
    def exit_handler(signo, frame):
        all_off()
        sys.exit(0)
    all_off()
    signal.signal(signal.SIGTERM, exit_handler)
    logging.info('Entering endless loop...')
    while True:
        if button.is_pressed():
            button_press_handler(solenoid_mux, led_mux, clock)


if __name__ == '__main__':
    main()
