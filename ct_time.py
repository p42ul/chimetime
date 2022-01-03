from time import sleep
from datetime import datetime


class CTTime:
    def get_current_time():
        time = datetime.now()
        hour, minute = time.hour, time.minute
        if hour > 12:
            hour -= 12
        return hour, minute

    def minute_to_closest_12th(minute: int):
        return round(minute / 5)
