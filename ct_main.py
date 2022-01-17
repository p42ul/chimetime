"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import CTButton, FakeButton
from ct_config import CTConfig
from ct_mappings import ct1_led_map, ct1_solenoid_map
from ct_mux import CTMux, FakeMux
from ct_time import CTTime

import argparse
import logging
import signal
import sys
from time import sleep


SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
CT_BUTTON_GPIO_PIN = 21

SOLENOID_ON_TIME = 0.1

MAJOR_ARP = [1, 3, 5, 8]

def button_press_handler(solenoid_mux, led_mux, clock, config):
    logging.debug('CT button press detected.')
    interdigit_delay = config['interdigit_delay']
    digits = clock.get_time_digits()
    if config['play_arp']:
        play_arp(solenoid_mux, config)
        sleep(config['arp_delay'])
    for d in digits:
        solenoid_mux.on(d)
        led_mux.on(d)
        sleep(SOLENOID_ON_TIME)
        solenoid_mux.off(d)
        led_mux.off(d)
        sleep(interdigit_delay)

def play_arp(solenoid_mux, config):
    arp_interdigit_delay = config['arp_interdigit_delay']
    for d in MAJOR_ARP:
        solenoid_mux.on(d)
        sleep(SOLENOID_ON_TIME)
        solenoid_mux.off(d)
        sleep(arp_interdigit_delay)

def init_i2c():
    import board
    import busio
    logging.info('Initializing I2C...')
    i2c = busio.I2C(board.SCL, board.SDA)
    logging.info('I2C initialized.')
    return i2c

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='Config file location.')
    parser.add_argument('--fake', default=False, action='store_true',
                        help='Use fakes (for testing).')
    return parser.parse_args()

def main():
    args = get_args()
    config = CTConfig(args.config)
    polling_interval = config['polling_interval']
    clock = CTTime()
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'config file path: {args.config}')
    logging.info('Starting Chime Time...')
    if args.fake:
        i2c = None
        solenoid_mux = FakeMux(i2c, SOLENOID_MUX_ADDR, ct1_solenoid_map)
        led_mux = FakeMux(i2c, LED_MUX_ADDR, ct1_led_map)
        button = FakeButton(CT_BUTTON_GPIO_PIN)
    else:
        i2c = init_i2c()
        solenoid_mux = CTMux(i2c, SOLENOID_MUX_ADDR, ct1_solenoid_map)
        led_mux = CTMux(i2c, LED_MUX_ADDR, ct1_led_map)
        button = CTButton(CT_BUTTON_GPIO_PIN)
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
            button_press_handler(solenoid_mux, led_mux, clock, config)
        sleep(polling_interval)


if __name__ == '__main__':
    main()
