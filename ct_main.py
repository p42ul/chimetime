"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import RealButton, FakeButton
from ct_config import CTConfig
from ct_mappings import ct1_led_map, ct1_solenoid_map
from ct_mux import RealMux, FakeMux
from ct_time import CTTime

import argparse
import logging
import signal
import sys
from time import sleep

logging.basicConfig(level=logging.DEBUG)

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
CT_BUTTON_GPIO_PIN = 21

SOLENOID_ON_TIME = 0.1

MAJOR_ARP = [1, 3, 5, 8]

class CT:
    def button_press_handler(self):
        logging.debug('CT button press detected.')
        interdigit_delay = self.config['interdigit_delay']
        digits = self.clock.get_time_digits()
        if self.config['play_arp']:
            self.play_arp()
            sleep(self.config['arp_delay'])
        for d in digits:
            self.solenoid_mux.on(d)
            self.led_mux.on(d)
            sleep(SOLENOID_ON_TIME)
            self.solenoid_mux.off(d)
            self.led_mux.off(d)
            sleep(interdigit_delay)

    def play_arp(self):
        arp_interdigit_delay = self.config['arp_interdigit_delay']
        for degree in MAJOR_ARP:
            self.solenoid_mux.on(degree)
            sleep(SOLENOID_ON_TIME)
            self.solenoid_mux.off(degree)
            sleep(arp_interdigit_delay)

    def init_i2c(self):
        import board
        import busio
        logging.info('Initializing I2C...')
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('I2C initialized.')
        return i2c

    def all_off(self):
        logging.info('Turning off all mux outputs.')
        for m in (self.solenoid_mux, self.led_mux):
            m.all_off()

    def __init__(self, config_path, fake=False):
        self.config = CTConfig(config_path, autoreload=True)
        self.polling_interval = self.config['polling_interval']
        self.clock = CTTime()
        logging.info('Starting Chime Time...')
        if not fake:
            self.i2c = self.init_i2c()
            Mux = RealMux
            Button = RealButton
        else:
            self.i2c = None
            Mux = FakeMux
            Button = FakeButton
        self.solenoid_mux = Mux(self.i2c, SOLENOID_MUX_ADDR, ct1_solenoid_map)
        self.led_mux = Mux(self.i2c, LED_MUX_ADDR, ct1_led_map)
        self.button = Button(CT_BUTTON_GPIO_PIN)
        def exit_handler(signo, frame):
            logging.info('detected signal {signal.strsignal(signo)}')
            all_off()
            sys.exit(0)
        self.all_off()
        signal.signal(signal.SIGTERM, exit_handler)

    def run(self):
        logging.info('entering main CT loop...')
        while True:
            if self.button.is_pressed():
                self.button_press_handler()
            sleep(self.polling_interval)
