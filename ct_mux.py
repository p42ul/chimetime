import logging


class CTMux:
    def __init__(self, i2c, address, mappings):
        from adafruit_mcp230xx.mcp23017 import MCP23017
        from digitalio import Direction
        logging.info(f'Initializing multiplexer at address {hex(address)}...')
        mux = MCP23017(i2c, address=address)
        logging.info(f'Multiplexer at address {hex(address)} initialized.')
        self.mux = mux
        self.mappings = mappings
        for i in self.mappings.values():
            pin = self.mux.get_pin(i)
            pin.direction = Direction.OUTPUT
            pin.value = False

    def _set(self, num: int, value: bool):
        pin = self.mappings[num]
        if pin is not None:
            self.mux.get_pin(pin).value = value

    def on(self, num: int):
        self._set(num, True)

    def off(self, num: int):
        self._set(num, False)

    def all_off(self):
        for pin in [self.mux.get_pin(p) for p in self.mappings.values()]:
            pin.value = False
        
class FakeMux:
    def __init__(self, i2c, address, mappings):
        logging.info(f'Initializing fake mux at address {hex(address)}...')
        self.mappings = mappings
        self.address = address

    def _set(self, num, value):
        pin = self.mappings[num]
        if pin is not None:
            logging.info(f'{hex(self.address)} {num} -> {pin} is now {value}')

    def on(self, num: int):
        self._set(num, True)

    def off(self, num: int):
        self._set(num, False)

    def all_off(self):
        for num in self.mappings.keys():
            self._set(num, False)
