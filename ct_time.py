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

    def get_time_digits(self):
        hour, minute = self.get_current_time()
        minute_digits = [int(d) for d in str(minute)]
        return [hour] + minute_digits
