from collections import namedtuple
from time import localtime, sleep
from typing import NewType

BPM = 180

class MusicError(Exception):
    pass

Chord = namedtuple('Chord', ['degrees', 'duration'])
Sequence = NewType('Sequence', list(Chord))

_time_sequences = {
        0: [],
        1: [Chord([1], 1)],
        2: [Chord([2], 1)],
        3: [Chord([3], 1)],
        4: [Chord([4], 1)],
        5: [Chord([5], 1)],
        6: [Chord([6], 1)],
        7: [Chord([7], 0.5), Chord([7], 0.5)],
        8: [Chord([8], 1)],
        9: [Chord([2, 7], 1)],
        10: [Chord([3, 7], 1)],
        11: [Chord([1], 0.5), Chord([1], 0.5), Chord([1], 1)],
        12: [Chord([5, 7], 1)],
        13: [Chord([1], 0.5), Chord([3], 1)],
        14: [Chord([1], 0.5), Chord([4], 1)],
        15: [Chord([1], 0.5), Chord([5], 1)],
        16: [Chord([1], 0.5), Chord([6], 1)],
        17: [Chord([1], 0.5), Chord([1], 0.5),  Chord([7], 1)],
        18: [Chord([1], 0.5), Chord([8], 1)],
        19: [Chord([1], 0.5), Chord([2, 7], 1)],
        20: [Chord([2], 0.5), Chord([2], 0.5)],
        30: [Chord([3], 0.5), Chord([3], 0.5)],
        40: [Chord([4], 0.5), Chord([4], 0.5)],
        50: [Chord([5], 0.5), Chord([5], 0.5)],
}

def _phoneticize_number(num: int) -> tuple(int, int):
    if num == 0:
        return []
    elif num > 0 and num < 10:
        return [0, num]
    elif num >= 10 and num < 20:
        return [num]
    elif num >= 20 and num < 60:
        # Only a tens digit.
        if num % 10 == 0:
            return [num]
        ones = num % 10
        tens = num - ones
        return (tens, ones)
    else:
        raise MusicError(f'Can only phoneticize numbers between 0-59, inclusive. Got: {num}')

def _play_chord(chord: Chord, degree_to_pin, solenoid_on_time):
    duration_secs = chord.duration / (BPM / 60)
    for p in (degree_to_pin(d) for d in chord.degrees):
        p.on()
    sleep(solenoid_on_time)
    for p in (degree_to_pin(d) for d in chord.degrees):
        p.off()
    sleep(duration_secs - solenoid_on_time)

def play_sequence(sequence: Sequence, degree_to_pin, solenoid_on_time):
    for chord in sequence:
        _play_chord(chord, degree_to_pin, solenoid_on_time)

def current_phonetic_time(now=None):
    if now is None:
        now = localtime()
    hours = _time_sequences[now.tm_hour] if now.tm_hour <=12 else _time_sequences[now.tm_hour - 12]
    minutes = sum([_time_sequences[n] for n in _phoneticize_number(now.tm_min)], [])
    return hours + minutes

def major_arppegio():
    return [Chord([1], 1), Chord([3], 0.25), Chord([5], 0.25), Chord([8], 0.25), Chord([], 2)]