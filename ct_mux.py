import platform
if platform.system() == 'Windows':
    import winsound

from abc import ABC, abstractmethod

import logging
import os

SOLENOID_MUX_ADDR = 0x20

class CTMux(ABC):
    @abstractmethod
    def on(self, num: int):
        pass

    @abstractmethod
    def off(self, num: int):
        pass

    @abstractmethod
    def all_off(self):
        pass

class RealMux(CTMux):
    def __init__(self, i2c, address, mappings):
        from adafruit_mcp230xx.mcp23017 import MCP23017
        from digitalio import Direction
        logging.info(f'Initializing multiplexer at address {hex(address)}...')
        mux = MCP23017(i2c, address=address)
        logging.info(f'Multiplexer at address {hex(address)} initialized.')
        self.mux = mux
        self.mappings = mappings
        for v in self.mappings.values():
            if v is None:
                continue
            pin = self.mux.get_pin(v)
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
        for num in self.mappings.keys():
            self._set(num, False)
class FakeMux(CTMux):
    def __init__(self, i2c, address, mappings):
        logging.info(f'Initializing fake mux at address {hex(address)}...')
        self.mappings = mappings
        self.address = address
        if self.address == SOLENOID_MUX_ADDR:
            self.tones = {num: os.path.abspath(f'tones/{num}.wav') for num in range(13)}
        # Needed to keep track of the state of the mux.
        self.state = {k: False for k in self.mappings.keys()}

    def _set(self, num, value):
        self.state[num] = value
        pin = self.mappings[num]
        if pin is not None:
            logging.info(f'{hex(self.address)} {num} -> {pin} is now {value}')

    def on(self, num: int):
        if self.address == SOLENOID_MUX_ADDR:
            winsound.PlaySound(self.tones[num], winsound.SND_FILENAME | winsound.SND_ASYNC)
        self._set(num, True)

    def off(self, num: int):
        self._set(num, False)

    def all_off(self):
        for num in self.mappings.keys():
            self._set(num, False)

    # Specific to LED ring, returns the current mux state in clock shape.
    def clock_display(self):
        led_states = {k: 'I' if v else 'O' for k, v in self.state.items()}
        l = lambda k: led_states[k]
        # Padded with x instead of space for readability.
        return (f'xxx{l(12)}xxx\n' +
                f'xx{l(11)}x{l(1)}xx\n' +
                f'x{l(10)}xxx{l(2)}x\n' +
                f'{l(9)}xxxxx{l(3)}\n' +
                f'x{l(8)}xxx{l(4)}x\n' +
                f'xx{l(7)}x{l(5)}xx\n' +
                f'xxx{l(6)}xxx').replace('x', ' ')

