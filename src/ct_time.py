import threading

from time import sleep
from datetime import datetime


class CTTime:
    def get_current_time(self):
        time = datetime.now()
        hour, minute = time.hour, time.minute
        if hour > 12:
            hour -= 12
        return hour, minute

    def minute_to_closest_12th(self, minute: int):
        return round(minute / 5)

    def get_time_digits(self) -> list:
        hour, minute = self.get_current_time()
        minute_digits = [int(d) for d in str(minute).zfill(2)]
        return [hour] + minute_digits

    def run_hourly(self, callback):
        def f():
            next_hour = datetime.now().hour + 1
            if next_hour > 12: # For 12-hour time.
                next_hour -= 12
            while True:
                now = datetime.now()
                hour = now.hour
                if hour > 12:
                    hour -= 12
                if hour >= next_hour:
                    callback(now)
                    next_hour = hour + 1
                sleep(1)
        t = threading.Thread(target=f, daemon=True)
        t.start()
        return t

