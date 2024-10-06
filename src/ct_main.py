from ct_button import FakeButton, RealButton
from config import Config
from constants import MAPPINGS_PATH, SOLENOID_MUX_ADDR, SOLENOID_ON_TIME, LED_MUX_ADDR, CT_BUTTON_GPIO_PIN, POLLING_INTERVAL, MAJOR_ARP
from ct_mux import FakeMux, RealMux

import atexit
from datetime import datetime
import json
import logging
import threading
from time import sleep

def init_i2c():
    import board
    import busio
    i2c = busio.I2C(board.SCL, board.SDA)
    logging.debug('I2C initialized.')
    return i2c

config = {
    'real':
    {
        'i2c': init_i2c,
        'mux': RealMux,
        'button': RealButton,
    },
    'fake':
    {
        'i2c': lambda: None,
        'mux': FakeMux,
        'button': FakeButton,
    }
}

class CT:
    def __init__(self, config_type: str):
        self.config = Config()
        solenoid_map, led_map = self.load_mappings(MAPPINGS_PATH, self.config['mapping'])
        self.i2c = config[config_type]['i2c']()
        self.solenoid_mux = config[config_type]['mux'](self.i2c, SOLENOID_MUX_ADDR, solenoid_map)
        self.led_mux = config[config_type]['mux'](self.i2c, LED_MUX_ADDR, led_map)
        self.button = config[config_type]['button'](CT_BUTTON_GPIO_PIN)
        self.all_off()
        atexit.register(self.all_off)

    def run(self):
        logging.debug('entering button detection loop.')
        while True:
            if self.button.is_pressed():
                self.chime_the_time()
            sleep(POLLING_INTERVAL)

    def led_off_delay(self, digit):
        delay = self.config['led_on_time']
        sleep(delay)
        self.led_mux.off(digit)

    def chime_the_time(self):
        interdigit_delay = self.config['interdigit_delay']
        digits = Time.get_time_digits()
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


    def all_off(self):
        logging.debug('Turning off all mux outputs.')
        for m in (self.solenoid_mux, self.led_mux):
            m.all_off()

    def load_mappings(self, path, mapping) -> tuple[dict, dict]:
        with open(path, 'r') as f:
            data = f.read()
        j = json.loads(data)[mapping]
        solenoids = {int(k): v for k,v in j['solenoid'].items()}
        leds = {int(k): v for k,v in j['led'].items()}
        return (solenoids, leds)


class Time:
    @staticmethod
    def get_current_time():
        time = datetime.now()
        hour, minute = time.hour, time.minute
        if hour > 12:
            hour -= 12
        return hour, minute

    @staticmethod
    def minute_to_closest_12th(minute: int):
        return round(minute / 5)

    @staticmethod
    def get_time_digits() -> list:
        hour, minute = Time.get_current_time()
        minute_digits = [int(d) for d in str(minute).zfill(2)]
        return [hour] + minute_digits