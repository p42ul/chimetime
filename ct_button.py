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
        self.pressed = False

    def is_pressed(self):
        if self.pressed:
            return False
        if input('enter any text to create fake button press, or nothing to continue...'):
            self.pressed = True
            return True
        return False
