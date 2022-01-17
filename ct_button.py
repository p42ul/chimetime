import logging
import random


class CTButton:
    def __init__(self, pin: int):
        from gpiozero import Button
        logging.info(f'Initializing CT button on GPIO pin {pin}...')
        self.button = Button(pin, pull_up=True)
        logging.info('CT button initialized.')

    def is_pressed(self):
        return self.button.is_pressed

class FakeButton:
    def __init__(self, pin):
        logging.info(f'Initializing fake CT button on pin {pin}...')

    def is_pressed(self):
        # Roll a six sided die.
        return random.randint(1,6) == 6
