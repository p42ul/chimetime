from collections import namedtuple
import heapq
import time

Event = namedtuple('Event', ['start_time', 'func', 'args'])

# Adapted from https://stackoverflow.com/questions/8875706/heapq-with-custom-compare-predicate
class EventHeap:
    def __init__(self):
        self._data = []
        self.index = 0

    def push(self, event):
        heapq.heappush(self._data, (event.start_time, self.index, event))
        self.index += 1

    def peek(self):
        if self._data:
            return self._data[0]
        return None

    def pop(self):
        return heapq.heappop(self._data)[2]

class Scheduler:
    def __init__(self, interrupt_func, interrupt_callback) -> None:
        self.schedule = EventHeap()
        self.interrupt_func = interrupt_func
        self.interrupt_callback = interrupt_callback

    def add(self, delay_secs, func, *args):
        event = self.make_event(delay_secs, func, *args)
        self.schedule.push(event)
        return self

    def make_event(self, delay_secs, func, *args):
        return Event(time.monotonic() + delay_secs, func, args)

    # Start the scheduler. Blocks forever.
    def run(self):
        while True:
            now = time.monotonic()
            irq = self.interrupt_func()
            if irq:
                self.interrupt_callback(irq)
            while True:
                if not self.schedule:
                    break
                maybe_event = self.schedule.peek()
                if not maybe_event:
                    break
                start_time, func, args = maybe_event
                if start_time > now:
                    break
                start_time, func, args = self.schedule.pop()
                func(*args)
