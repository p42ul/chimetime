import logging

from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction

class CTMux:
    def __init__(self, i2c, address, num_pins):
        logging.info(f'Initializing multiplexer at address {hex(address)}...')
        mux = MCP23017(i2c, address=address)
        logging.info(f'Multiplexer at address {hex(address)} initialized.')
        self.mux = mux
        self.num_pins = num_pins
        for i in range(self.num_pins):
            pin = self.mux.get_pin(i)
            pin.direction = Direction.OUTPUT
            pin.value = False

    def set(self, pin: int, value: bool):
        self.mux.get_pin(pin).value = value

    def on(self, pin: int):
        self.set(pin, True)

    def off(self, pin: int):
        self.set(pin, False)

    def all_off(self):
        for i in range(self.num_pins):
            self.off(i)
