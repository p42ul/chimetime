"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_mappings import CT_BUTTON_GPIO_PIN, LEDS, SOLENOIDS

import atexit
from time import sleep

import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction
from gpiozero import Button

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
MUX_NUM_PINS = 16
POLLING_INTERVAL = 1

def sound_time(solenoid_mux, led_mux):
    print('button was pressed')
    pass

def mux_all_pins_off(mux, num_pins):
    for p in [mux.get_pin(i) for i in range(num_pins)]:
        p.direction = Direction.OUTPUT
        p.value = False

def main():
    print('hello')
    i2c = busio.I2C(board.SCL, board.SDA)
    solenoid_mux = MCP23017(i2c, address=SOLENOID_MUX_ADDR)
    led_mux = MCP23017(i2c, address=LED_MUX_ADDR)
    ct_button = Button(CT_BUTTON_GPIO_PIN, pull_up=True)
    def all_off():
        for m in (solenoid_mux, led_mux):
            mux_all_pins_off(m, MUX_NUM_PINS)
    all_off()
    atexit.register(all_off)
    while True:
        if ct_button.is_pressed:
            sound_time(solenoid_mux, led_mux)
        sleep(POLLING_INTERVAL)

if __name__ == '__main__':
    main()