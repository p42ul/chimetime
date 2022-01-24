"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import RealButton, FakeButton
from ct_config import CTConfig
from ct_mappings import ct1_led_map, ct1_solenoid_map
from ct_mux import RealMux, FakeMux
from ct_time import CTTime

import argparse
import atexit
from datetime import datetime
import logging
import sys
import threading
from time import sleep

logging.basicConfig(level=logging.DEBUG)

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
CT_BUTTON_GPIO_PIN = 21

SOLENOID_ON_TIME = 0.1
POLLING_INTERVAL = 0.01

MAJOR_ARP = [1, 3, 5, 8]

class CT:
    def chime_the_time(self):
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

    def play_grandfather(self, dt: datetime):
        if not self.config['grandfather_mode']:
            return
        hour = dt.hour
        if hour > 12:
            hour -= 12
        delay = self.config['grandfather_delay']
        for _ in range(hour):
            self.solenoid_mux.on(0)
            sleep(SOLENOID_ON_TIME)
            self.solenoid_mux.off(0)
            sleep(delay)

    def play_arp(self):
        arp_interdigit_delay = self.config['arp_interdigit_delay']
        for degree in MAJOR_ARP:
            self.solenoid_mux.on(degree)
            sleep(SOLENOID_ON_TIME)
            self.solenoid_mux.off(degree)
            sleep(arp_interdigit_delay)

    def play_test(self):
        for k in ct1_solenoid_map:
            self.solenoid_mux.on(k)
            sleep(SOLENOID_ON_TIME)
            self.solenoid_mux.off(k)
            sleep(self.config['interdigit_delay'])

    def init_i2c(self):
        import board
        import busio
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.debug('I2C initialized.')
        return i2c

    def all_off(self):
        logging.debug('Turning off all mux outputs.')
        for m in (self.solenoid_mux, self.led_mux):
            m.all_off()

    def __init__(self, config_path, fake=False):
        self.config = CTConfig(config_path)
        self.clock = CTTime()
        self.solenoid_mux = None
        self.led_mux = None
        self.button = None
        # We just run this, and it checks the config at chime time.
        self.clock.run_hourly(self.play_grandfather)
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
        self.all_off()
        atexit.register(self.all_off)

    def run(self):
        logging.debug('entering button detection loop.')
        while True:
            if self.button.is_pressed():
                self.chime_the_time()
            sleep(POLLING_INTERVAL)
