from ct_time import CTTime

import logging


class CTLED:
    def __init__(self, mux)
        self.mux = mux
        self.POLL_INTERVAL = 1

    def run(self):
        logging.info('Starting LED clock...')
        clock = CTTime()
        while True:
            mux.all_off()
            hour_pin, minute = clock.get_current_time()
            minute_pin = clock.minute_to_closest_12th(minute)
            self.mux.all_off()
            self.mux.on(hour_pin)
            self.mux.on(minute_pin)
            sleep(self.POLL_INTERVAL)
