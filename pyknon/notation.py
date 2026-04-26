import re


REGEX_NOTE = re.compile("([a-gA-GRr])([b#]*)([0-9]*)([.]*)([',]*)")
NOTE_NAMES = "c # d # e f # g # a # b".split()


class NotationError(Exception):
    pass


def parse_accidental(acc):
    pass


def parse_octave(string):
    """5 is central octave. Return 5 as a fall-back"""
    pass


def parse_dur(dur, dots=""):
    pass


def note_number(pitch, acc):
    pass


def parse_note(note, volume=120, prev_octave=5, prev_dur=0.25):
    pass


def parse_notes(notes, volume=120):
    # (number, octave, dur, volume)
    pass
