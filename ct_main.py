"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import RealButton, FakeButton
from ct_config import CTConfig
from ct_constants import SOLENOID_MUX_ADDR, SOLENOID_ON_TIME, LED_MUX_ADDR, CT_BUTTON_GPIO_PIN, POLLING_INTERVAL, MAJOR_ARP
from ct_mux import RealMux, FakeMux
from ct_time import CTTime

import atexit
from datetime import datetime
import json
import logging
import sys
import threading
from time import sleep


class CT:
    def led_off_delay(self, digit):
        delay = self.config['led_on_time']
        sleep(delay)
        self.led_mux.off(digit)

    def chime_the_time(self):
        interdigit_delay = self.config['interdigit_delay']
        digits = self.clock.get_time_digits()
        sleep(self.config['pre_delay'])
        if self.config['play_arp']:
            self.play_arp()
            sleep(self.config['arp_delay'])
        for d in digits:
            self.flash_led(d)
            self.play_note(d)
            sleep(interdigit_delay)

    def play_grandfather(self, dt: datetime):
        if not self.config['grandfather_mode']:
            return
        hour = dt.hour
        if hour > 12:
            hour -= 12
        delay = self.config['grandfather_delay']
        for _ in range(hour):
            self.play_note(0)
            sleep(delay)

    def play_arp(self):
        arp_interdigit_delay = self.config['arp_interdigit_delay']
        for degree in MAJOR_ARP:
            self.play_note(degree)
            sleep(arp_interdigit_delay)

    def play_note(self, d):
        self.solenoid_mux.on(d)
        sleep(SOLENOID_ON_TIME)
        self.solenoid_mux.off(d)

    def flash_led(self, d):
        self.led_mux.on(d)
        threading.Thread(target=self.led_off_delay, args=[d]).start()


    def play_test(self):
        for d in range(12 + 1):
            self.flash_led(d)
            self.play_note(d)
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

    def load_mapping(self, path, mapping) -> (dict, dict):
        with open(path, 'r') as f:
            data = f.read()
        j = json.loads(data)
        j = j[mapping]
        solenoids = {int(k): v for k,v in j['solenoid'].items()}
        leds = {int(k): v for k,v in j['led'].items()}
        return (solenoids, leds)


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
        solenoid_map, led_map = self.load_mapping('mappings.json', self.config['mapping'])
        self.solenoid_mux = Mux(self.i2c, SOLENOID_MUX_ADDR, solenoid_map)
        self.led_mux = Mux(self.i2c, LED_MUX_ADDR, led_map)
        self.button = Button(CT_BUTTON_GPIO_PIN)
        self.all_off()
        atexit.register(self.all_off)

    def run(self):
        logging.debug('entering button detection loop.')
        while True:
            if self.button.is_pressed():
                self.chime_the_time()
            sleep(POLLING_INTERVAL)
