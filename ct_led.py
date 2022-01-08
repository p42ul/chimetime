from ct_time import CTTime

import logging


class CTLED:
    def __init__(self, mux):
        self.mux = mux
        self.clock = CTTime()

    def update(self):
        self.mux.all_off()
        hour_pin, minute = self.clock.get_current_time()
        minute_pin = self.clock.minute_to_closest_12th(minute)
        self.mux.all_off()
        self.mux.on(hour_pin)
        self.mux.on(minute_pin)
