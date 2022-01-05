import logging

class CTButton:
    def __init__(self, pin: int):
        logging.info(f'Initializing CT button on GPIO pin {pin}...')
        self.button = Button(pin, pull_up=True)
        logging.info('CT button initialized.')

    def is_pressed(self):
        return self.button.is_pressed
