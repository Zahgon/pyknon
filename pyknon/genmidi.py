from pyknon.MidiFile import MIDIFile
from pyknon.music import Note, NoteSeq, Rest


class MidiError(Exception):
    pass


class Midi:
    def __init__(self, number_tracks=1, tempo=60, instrument=0, channel=None):
        """
        instrument: can be an integer or a list
        channel: can be an integer or a list
        """

        self.number_tracks = number_tracks
        self.midi_data = MIDIFile(number_tracks)

        for track in range(number_tracks):
            self.midi_data.addTrackName(track, 0, "Track {0}".format(track))
            self.midi_data.addTempo(track, 0, tempo)
            instr = instrument[track] if isinstance(instrument, list) else instrument
            if channel is None:
                _channel = track
            elif isinstance(channel, list):
                _channel = channel[track]
            else:
                _channel = channel
            self.midi_data.addProgramChange(track, _channel, 0, instr)

    def seq_chords(self, seqlist, track=0, time=0, channel=None):
        pass

    def seq_notes(self, noteseq, track=0, time=0, channel=None):
        pass

    def change_tuning(self, track, tunings, real_time=False, tuning_program=0):
        pass

    def write(self, filename):
        pass
