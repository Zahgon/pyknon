"""
A simple numeric library for music computation.

This module is good for teaching, demonstrations, and quick hacks. To
generate actual music you should use the music module.

"""

from itertools import combinations, chain
from fractions import Fraction


def mod12(n):
    pass


def interval(x, y):
    pass


def interval_class(x, y):
    pass


def intervals(notes):
    pass


def all_intervals(notes):
    pass


def transposition(notes, index):
    pass


def transposition_startswith(notes, start):
    pass


def is_related_by_transposition(notes1, notes2):
    pass


def inversion(notes, index=0):
    pass


def inversion_startswith(notes, start):
    pass


def inversion_first_note(notes):
    pass


def rotate(notes, n=1):
    pass


def rotate_set(notes):
    pass


def retrograde(notes):
    pass


def note_name(number):
    pass


def notes_names(notes):
    pass


def accidentals(note_string):
    pass


def name_to_number(note_string):
    pass


def name_to_diatonic(note_string):
    pass


def note_duration(note_value, unity, tempo):
    pass


def dotted_duration(duration, dots):
    pass


def durations(notes_values, unity, tempo):
    pass


def get_quality(diatonic_interval, chromatic_interval):
    pass


def interval_name(note1, note2):
    pass
