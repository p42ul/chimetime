"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import CTButton
from ct_mappings import ct1_solenoid_map
from ct_mux import CTMux
from ct_time import CTTime
from ct_led import CTLED

import atexit
import logging
from time import sleep

import board
import busio
from gpiozero import Button

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
CT_BUTTON_GPIO_PIN = 21
POLLING_INTERVAL = 1
SOLENOID_ON_TIME = 0.1
INTERDIGIT_DELAY = 0.5

def button_press_handler(solenoid_mux, clock):
    logging.debug('CT button press detected.')
    digits = clock.get_time_digits()
    for d in digits:
        pin = ct1_solenoid_map[d]
        solenoid_mux.on(pin)
        sleep(SOLENOID_ON_TIME)
        solenoid_mux.off(pin)
        sleep(INTERDIGIT_DELAY)

def init_i2c():
    logging.info('Initializing I2C...')
    i2c = busio.I2C(board.SCL, board.SDA)
    logging.info('I2C initialized.')
    return i2c

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting Chime Time...')
    i2c = init_i2c()
    solenoid_mux = CTMux(i2c, SOLENOID_MUX_ADDR, 16)
    led_mux = CTMux(i2c, LED_MUX_ADDR, 12)
    led_controller = CTLED(led_mux)
    button = CTButton(CT_BUTTON_GPIO_PIN)
    clock = CTTime()
    def all_off():
        logging.info('Turning off all mux outputs on exit...')
        for m in (solenoid_mux, led_mux):
            m.all_off()
    all_off()
    atexit.register(all_off)
    logging.info('Entering endless loop...')
    while True:
         led_controller.update()
        if button.is_pressed():
            button_press_handler(solenoid_mux, clock)
        sleep(POLLING_INTERVAL)


if __name__ == '__main__':
    main()
