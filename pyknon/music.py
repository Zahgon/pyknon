from collections.abc import MutableSequence, Iterable
import copy
from pyknon import notation


class MusiclibError(Exception):
    pass


class Rest:
    def __init__(self, dur=0.25):
        self.dur = dur

    def __repr__(self):
        return "<R: {0}>".format(self.dur)

    def __eq__(self, other):
        return self.dur == other.dur

    @property
    def verbose(self):
        pass

    @property
    def midi_dur(self):
        # The MIDI library uses 1 for quarter note but we use 0.25
        pass

    def stretch_dur(self, factor):
        pass


class Note:
    def __init__(self, value=0, octave=5, dur=0.25, volume=100):
        if isinstance(value, str):
            self.value, self.octave, self.dur, self.volume = notation.parse_note(value)
        else:
            offset, val = divmod(value, 12)
            self.value = val
            self.octave = octave + offset
            self.dur = dur
            self.volume = volume

    def __eq__(self, other):
        return self.value == other.value and self.dur == other.dur and self.octave == other.octave

    def __sub__(self, other):
        return self.midi_number - other.midi_number

    def __repr__(self):
        return "<{0}>".format(self.name)

    @property
    def verbose(self):
        pass

    @property
    def name(self):
        pass

    @property
    def midi_number(self):
        pass

    @property
    def midi_dur(self):
        # The MIDI library uses 1 for quarter note but we use 0.25
        pass

    def __note_octave(self, octave):
        """Return a note value in terms of a given octave octave

           n = Note(11, 4)
           __note_octave(n, 5) = -1
        """
        pass

    def transposition(self, index):
        pass

    ## FIXME: transpose down
    def tonal_transposition(self, index, scale):
        pass

    def harmonize(self, scale, interval=3, size=3):
        pass

    def inversion(self, index=0, initial_octave=None):
        pass

    def stretch_dur(self, factor):
        pass


class NoteSeq(MutableSequence):  # pylint: disable=too-many-ancestors
    @staticmethod
    def _is_note_or_rest(args):
        pass

    @staticmethod
    def _make_note_or_rest(note_list):
        pass

    @staticmethod
    def _parse_score(filename):
        pass

    def __init__(self, args=None):
        if isinstance(args, str):
            if args.startswith("file://"):
                filename = args.replace("file://", "")
                note_lists = notation.parse_notes(self._parse_score(filename))
            else:
                note_lists = notation.parse_notes(args.split())
            self.items = [self._make_note_or_rest(x) for x in note_lists]
        elif isinstance(args, Iterable):
            if self._is_note_or_rest(args):
                self.items = args
            else:
                raise MusiclibError("Every argument have to be a Note or a Rest.")
        elif args is None:
            self.items = []
        else:
            raise MusiclibError("NoteSeq doesn't accept this type of data.")

    def __iter__(self):
        for x in self.items:
            yield x

    def __delitem__(self, i):
        del self.items[i]

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.items[i]
        else:
            return NoteSeq(self.items[i])

    def __len__(self):
        return len(self.items)

    def __setitem__(self, i, value):
        self.items[i] = value

    def __repr__(self):
        return "<Seq: {0}>".format(self.items)

    def __eq__(self, other):
        if len(self) == len(other):
            return all(x == y for x, y in zip(self.items, other.items))

    def __add__(self, other):
        if isinstance(other, NoteSeq):
            return NoteSeq(self.items + other.items)
        elif isinstance(other, (Note, Rest)):
            return NoteSeq(self.items + [other])

    def __radd__(self, other):
        if isinstance(other, NoteSeq):
            #  This should never be called because the other NoteSeq should
            #  handle the concatenation, but it's here for completness sake
            return NoteSeq(other.items + self.items)
        elif isinstance(other, (Note, Rest)):
            return NoteSeq([other] + self.items)

    def __mul__(self, n):
        return NoteSeq(self.items * n)

    @property
    def verbose(self):
        pass

    def retrograde(self):
        pass

    def insert(self, key, value):
        pass

    def transposition(self, index):
        pass

    @staticmethod
    def _make_note(item):
        pass

    def transposition_startswith(self, note_start):
        pass

    def inversion(self, index=0):
        pass

    def inversion_startswith(self, note_start):
        pass

    def harmonize(self, interval=3, size=3):
        pass

    def rotate(self, n=1):
        pass

    def stretch_dur(self, factor):
        pass

    ## TODO: gives an error with rests
    def intervals(self):
        pass

    def stretch_interval(self, factor):
        pass

    # Aliases
    transp = transposition_startswith
    inv = inversion_startswith
