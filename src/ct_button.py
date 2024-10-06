from abc import ABC, abstractmethod
import logging


class CTButton(ABC):
    @abstractmethod
    def is_pressed(self) -> bool:
        pass

class RealButton(CTButton):
    def __init__(self, pin: int):
        from gpiozero import Button
        logging.info(f'Initializing CT button on GPIO pin {pin}...')
        self.button = Button(pin, pull_up=True)
        logging.info('CT button initialized.')

    def is_pressed(self):
        return self.button.is_pressed

class FakeButton(CTButton):
    def __init__(self, pin):
        logging.info(f'Initializing fake CT button on pin {pin}...')

    def is_pressed(self):
        input('waiting for input to create fake button press...\n')
        return True
