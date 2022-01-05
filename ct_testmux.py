from gpiozero import LED

import logging


class CTMux:
    def __init__(self, _i2c, _address, _num_pins):
        logging.info('Initializing test mux...')
        self.solenoid_map = {i: LED(e) for i, e in enumerate((17, 27, 22, 5, 6, 13, 19, 26))}

    def set(self, pin: int, value: bool):
        if value:
            self.on(pin)
        else:
            self.off(pin)

    def on(self, pin):
        self.solenoid_map[pin].on()

    def off(self, pin):
        self.solenoid_map[pin].off()

    def all_off(self):
        for p in self.solenoid_map.values():
            p.off()