"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_mappings import ct_button_gpio_pin, solenoid_map
from ct_music import play_sequence, current_phonetic_time

import atexit
import logging
from time import sleep

import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction
from gpiozero import Button

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
MUX_NUM_PINS = 16
POLLING_INTERVAL = 1
SOLENOID_ON_TIME = 0.1


def on_func_factory(solenoid_mux):
    def f(d):
        pin = solenoid_map[d]
        solenoid_mux.get_pin(pin).value = True
        logging.debug(f'Pin {pin} is on.')
    return f


def off_func_factory(solenoid_mux):
    def f(d):
        pin = solenoid_map[d]
        solenoid_mux.get_pin(pin).value = False
        logging.debug(f'Pin {pin} is off.')
    return f


def button_press_handler(solenoid_mux):
    logging.debug('CT button press detected.')
    current_time = current_phonetic_time()
    play_sequence(current_time, on_func_factory(solenoid_mux), off_func_factory(solenoid_mux), SOLENOID_ON_TIME)


def mux_all_off(mux, num_pins, value=False):
    for p in [mux.get_pin(i) for i in range(num_pins)]:
        p.direction = Direction.OUTPUT
        p.value = value


def init_i2c():
    logging.info('Initializing I2C...')
    i2c = busio.I2C(board.SCL, board.SDA)
    logging.info('I2C initialized.')
    return i2c


def init_mux(i2c, address):
    logging.info(f'Initializing multiplexer at address {hex(address)}...')
    mux = MCP23017(i2c, address=address)
    logging.info(f'Multiplexer at address {hex(address)} initialized.')
    return mux


def init_ct_button(pin):
    logging.info(f'Initializing CT button on GPIO pin {pin}...')
    ct_button = Button(ct_button_gpio_pin, pull_up=True)
    logging.info('CT button initialized.')
    return ct_button


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting Chime Time...')
    i2c = init_i2c()
    solenoid_mux = init_mux(i2c, SOLENOID_MUX_ADDR)
    led_mux = init_mux(i2c, LED_MUX_ADDR)
    ct_button = init_ct_button(ct_button_gpio_pin)

    def all_off():
        logging.info('Turning off all mux pins...')
        for m in (solenoid_mux, led_mux):
            mux_all_off(m, MUX_NUM_PINS)
        logging.info('All mux pins turned off.')
    all_off()
    atexit.register(all_off)
    logging.info('Entering endless loop...')
    while True:
        # if ct_button.is_pressed:
        if True:
            button_press_handler(solenoid_mux)
        sleep(POLLING_INTERVAL)


if __name__ == '__main__':
    main()
