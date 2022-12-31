from collections import namedtuple
from time import sleep

Note = namedtuple('Note', ['degree', 'length'])

# Musical helper functions
def Qd(degree):
    return Note(degree, 1.5)

def Q(degree):
    return Note(degree, 1.0)

def E(degree):
    return Note(degree, 0.5)

BPM = 100
REST = -1

class Music:
    def __init__(self, play_func):
        self.play = play_func
        self.tempo = 1 / (BPM/60)

    def _is_rest(self, note):
        return note.degree == REST

    def play_sequence(self, seq):
        print(seq)
        for note in seq:
            if not self._is_rest(note):
                self.play(note.degree)
            sleep(self.tempo*note.length)

    def auld(self):
        seq = (
            Q(1), Qd(4), E(3), Q(4), Q(6), Qd(5), E(4), Q(5), Q(6),
            Qd(4), E(4), Q(6), Q(8), Q(9), Q(REST), Q(REST), Q(9),
            Qd(8), E(6), Q(6), Q(4), Qd(5), E(4), Q(5), E(6), E(5),
            Qd(4), E(2), Q(2), Q(1), Q(4), Q(REST), Q(REST),
            Q(9), E(8), Qd(6), E(6), Qd(4), Qd(5), E(4), Q(5), Q(9),
            E(8), Qd(6), E(6), Qd(8), Q(9), Q(REST), Q(REST), Q(9),
            Qd(8), E(6), Q(6), Q(4), Qd(5), E(4), Q(5),
            E(6), E(5), Qd(4), E(2), Q(2), Q(1), Q(4),
        )
        self.play_sequence(seq)

