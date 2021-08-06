from time import sleep
from datetime import datetime

def get_current_time():
    time = datetime.now()
    hour, minute = time.hour, time.minute
    if hour > 12:
        hour -= 12
    return hour, minute


def minute_to_closest_12th(minute):
    return round(minute / 5)

def illuminate_leds(mux, leds)
    for l in leds:
        mux.get_pin(l).value = True
    sleep(1)
    for l in leds:
        mux.get_pin(l).value = False
