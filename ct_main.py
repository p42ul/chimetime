"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_button import RealButton, FakeButton
from ct_config import CTConfig
from ct_constants import MAPPINGS_PATH, SOLENOID_MUX_ADDR, SOLENOID_ON_TIME, LED_MUX_ADDR, CT_BUTTON_GPIO_PIN, MAJOR_ARP
from ct_mux import RealMux, FakeMux
from ct_scheduler import Scheduler

from datetime import datetime
import argparse
import atexit
import json
import logging

class CT:
    def __init__(self, fake=False):
        self.config = CTConfig()

        if not fake:
            self.i2c = self._init_i2c()
            Mux = RealMux
            Button = RealButton
        else:
            self.i2c = None
            Mux = FakeMux
            Button = FakeButton

        solenoid_map, led_map = self._load_mappings(MAPPINGS_PATH, self.config['mapping'])
        self._solenoid_mux = Mux(self.i2c, SOLENOID_MUX_ADDR, solenoid_map)
        self._led_mux = Mux(self.i2c, LED_MUX_ADDR, led_map)
        self._button = Button(CT_BUTTON_GPIO_PIN)

        self._all_off()
        atexit.register(self._all_off)

        self._is_active = False
        self._scheduler = Scheduler(self._button.is_pressed, self._irq_handler)
        self._scheduler.run() # Blocks forever

    def chime_the_time(self):
        if self._is_active:
            return
        self._set_active(True)
        pre_delay = self.config['pre_delay']
        arp_delay = self.config['arp_delay']
        led_on_time = self.config['led_on_time']
        if self.config['play_arp']:
            arp_time = self._play_arp(pre_delay) + arp_delay
        else:
            arp_time = pre_delay
        note_time = self._play_digits(arp_time)
        self._scheduler.add(note_time + led_on_time, self._set_active, False)

    def play_test(self):
        counter = 0
        for d in range(12 + 1):
            self._play_note(counter, d)
            counter += self.config['interdigit_delay']

    def _irq_handler(self, irq):
        self.chime_the_time()

    def _set_active(self, val):
        word = 'active' if val else 'inactive'
        print(f'clock is now {word}')
        self._is_active = val

    def _play_digits(self, offset):
        interdigit_delay = self.config['interdigit_delay']
        digits = self._get_time_digits()
        counter = 0
        for d in digits:
            self._play_note(counter + offset, d)
            counter += interdigit_delay
        return counter + offset

    def _play_arp(self, offset):
        arp_interdigit_delay = self.config['arp_interdigit_delay']
        counter = 0
        for d in MAJOR_ARP:
            self._play_note(counter + offset, d, with_led=False)
            counter += arp_interdigit_delay
        return counter

    def _play_note(self, start_time, d, with_led=True):
        led_on_time = self.config['led_on_time']
        self._scheduler.add(start_time, self._solenoid_mux.on, d)
        self._scheduler.add(start_time + SOLENOID_ON_TIME, self._solenoid_mux.off, d)
        if with_led:
            self._scheduler.add(start_time, self._led_mux.on, d)
            self._scheduler.add(start_time + led_on_time, self._led_mux.off, d)

    def _init_i2c(self):
        import board
        import busio
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.debug('I2C initialized.')
        return i2c

    def _all_off(self):
        logging.debug('Turning off all mux outputs.')
        for m in (self._solenoid_mux, self._led_mux):
            m.all_off()

    def _load_mappings(self, path, mapping) -> (dict, dict):
        with open(path, 'r') as f:
            data = f.read()
        j = json.loads(data)[mapping]
        solenoids = {int(k): v for k,v in j['solenoid'].items()}
        leds = {int(k): v for k,v in j['led'].items()}
        return (solenoids, leds)

    def _get_time_digits(self) -> list:
        time = datetime.now()
        hour, minute = time.hour, time.minute
        if hour > 12:
            hour -= 12
        minute_digits = [int(d) for d in str(minute).zfill(2)]
        return [hour] + minute_digits


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fake", action="store_true", help="If set, does not use real multiplexers.")
    args = parser.parse_args()

    ct = CT(fake=args.fake)