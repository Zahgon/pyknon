#-----------------------------------------------------------------------------
# Name:        MidiFile.py
# Purpose:     MIDI file manipulation utilities
#
# Author:      Mark Conway Wirt <emergentmusics) at (gmail . com>
#
# Created:     2008/04/17
# Copyright:   (c) 2009 Mark Conway Wirt
# License:     Please see License.txt for the terms under which this
#              software is distributed.
#-----------------------------------------------------------------------------

import struct
import sys
import math

PYTHON3 = True if sys.version_info[0] == 3 else False


# TICKSPERBEAT is the number of "ticks" (time measurement in the MIDI file) that
# corresponds to one beat. This number is somewhat arbitrary, but should be chosen
# to provide adequate temporal resolution.

TICKSPERBEAT = 128

controllerEventTypes = {
                        'pan' : 0x0a
                        }
class MIDIEvent:
    '''
    The class to contain the MIDI Event (placed on MIDIEventList.
    '''
    def __init__(self):
        self.type='unknown'
        self.time=0
        self.ord = 0
        
    def __lt__(self, other):
        ''' Sorting function for events.'''
        if self.time < other.time:
            return True
        elif self.time > other.time:
            return False
        else:
            if self.ord < other.ord:
                return True
            elif self.ord > other.ord:
                return False
            else:
                return False

    def __cmp__(self, other):
        ''' Sorting function for events.'''
        if self.time < other.time:
            return -1
        elif self.time > other.time:
            return 1
        else:
            if self.ord < other.ord:
                return -1
            elif self.ord > other.ord:
                return 1
            else:
                return 0

class GenericEvent():
    '''The event class from which specific events are derived
    '''
    def __init__(self,time):
        self.time = time 
        self.type = 'Unknown'


        
    def __eq__(self, other):
        '''
        Equality operator for Generic Events and derived classes.
        
        In the processing of the event list, we have need to remove duplicates. To do this
        we rely on the fact that the classes are hashable, and must therefore have an 
        equality operator (__hash__() and __eq__() must both be defined).
        
        This is the most embarrassing portion of the code, and anyone who knows about OO
        programming would find this almost unbelievable. Here we have a base class that
        knows specifics about derived classes, thus breaking the very spirit of 
        OO programming.
        
        I suppose I should go back and restructure the code, perhaps removing the derived
        classes altogether. At some point perhaps I will.
        '''
        if self.time != other.time or self.type != other.type:
            return False
            
        # What follows is code that encodes the concept of equality for each derived 
        # class. Believe it f you dare.
        
        if self.type == 'note':
            if self.pitch != other.pitch or self.channel != other.channel:
                return False
        if self.type == 'tempo':
            if self.tempo != other.tempo:
                return False
        if self.type == 'programChange':
            if self.programNumber != other.programNumber or self.channel != other.channel:
                return False
        if self.type == 'trackName':
            if self.trackName != other.trackName:
                return False
        if self.type == 'controllerEvent':
            if self.parameter1 != other.parameter1 or \
                self.parameter2 != other.parameter2 or \
                self.channel != other.channel or \
                self.eventType != other.eventType:
                return False
                
        if self.type == 'SysEx':
            if self.manID != other.manID:
                return False
                
        if self.type == 'UniversalSysEx':
            if self.code != other.code or\
                self.subcode != other.subcode or \
                self.sysExChannel != other.sysExChannel:
                return False
                
        return True
        
    def __hash__(self):
        '''
        Return a hash code for the object.
        
        This is needed for the removal of duplicate objects from the event list. The only
        real requirement for the algorithm is that the hash of equal objects must be equal.
        There is probably great opportunity for improvements in the hashing function.
        '''
        # Robert Jenkin's 32 bit hash.
        a = int(self.time)
        a = (a+0x7ed55d16) + (a<<12)
        a = (a^0xc761c23c) ^ (a>>19)
        a = (a+0x165667b1) + (a<<5)
        a = (a+0xd3a2646c) ^ (a<<9)
        a = (a+0xfd7046c5) + (a<<3)
        a = (a^0xb55a4f09) ^ (a>>16)
        return a

class MIDITrack:
    '''A class that encapsulates a MIDI track
    '''
    # Nested class definitions.
    
    class note(GenericEvent):
        '''A class that encapsulates a note
        '''
        def __init__(self,channel, pitch,time,duration,volume):
            
            GenericEvent.__init__(self,time)
            self.pitch = pitch
            self.duration = duration
            self.volume = volume
            self.type = 'note'
            self.channel = channel
            
        def compare(self, other):
            '''Compare two notes for equality.
            '''
            pass
                    
            
    class tempo(GenericEvent):
        '''A class that encapsulates a tempo meta-event
        '''
        def __init__(self,time,tempo):
            
            GenericEvent.__init__(self,time)
            self.type = 'tempo'
            self.tempo = int(60000000 / tempo)
            
    class programChange(GenericEvent):
        '''A class that encapsulates a program change event.
        '''
        
        def __init__(self,  channel,  time,  programNumber):
            GenericEvent.__init__(self, time,)
            self.type = 'programChange'
            self.programNumber = programNumber
            self.channel = channel
            
    class SysExEvent(GenericEvent):
        '''A class that encapsulates a System Exclusive  event.
        '''
        
        def __init__(self,  time,  manID,  payload):
            GenericEvent.__init__(self, time,)
            self.type = 'SysEx'
            self.manID = manID
            self.payload = payload
            
    class UniversalSysExEvent(GenericEvent):
        '''A class that encapsulates a Universal System Exclusive  event.
        '''
        
        def __init__(self,  time,  realTime,  sysExChannel,  code,  subcode,  payload):
            GenericEvent.__init__(self, time,)
            self.type = 'UniversalSysEx'
            self.realTime = realTime
            self.sysExChannel = sysExChannel
            self.code = code
            self.subcode = subcode
            self.payload = payload
            
    class ControllerEvent(GenericEvent):
        '''A class that encapsulates a program change event.
        '''
        
        def __init__(self,  channel,  time,  eventType,  parameter1,):
            GenericEvent.__init__(self, time,)
            self.type = 'controllerEvent'
            self.parameter1 = parameter1
            self.channel = channel
            self.eventType = eventType

    class trackName(GenericEvent):
        '''A class that encapsulates a program change event.
        '''
        
        def __init__(self,  time,  trackName):
            GenericEvent.__init__(self, time,)
            self.type = 'trackName'
            self.trackName = trackName

            
    def __init__(self, removeDuplicates,  deinterleave):
        '''Initialize the MIDITrack object.
        '''
        self.headerString = struct.pack('cccc',b'M',b'T',b'r',b'k')
        self.dataLength = 0 # Is calculated after the data is in place
        if PYTHON3:
            self.MIDIdata = b""
        else:
            self.MIDIdata = ""
        self.closed = False
        self.eventList = []
        self.MIDIEventList = []
        self.remdep = removeDuplicates
        self.deinterleave = deinterleave
        
    def addNoteByNumber(self,channel, pitch,time,duration,volume):
        '''Add a note by chromatic MIDI number
        '''
        pass
        
    def addControllerEvent(self,channel,time,eventType, paramerter1):
        '''
        Add a controller event.
        '''
        pass
        
    def addTempo(self,time,tempo):
        '''
        Add a tempo change (or set) event.
        '''
        pass
        
    def addSysEx(self,time,manID, payload):
        '''
        Add a SysEx event.
        '''
        pass
        
    def addUniversalSysEx(self,time,code, subcode, payload,  sysExChannel=0x7F,  \
        realTime=False):
        '''
        Add a Universal SysEx event.
        '''
        pass
        
    def addProgramChange(self,channel, time, program):
        '''
        Add a program change event.
        '''
        pass
        
    def addTrackName(self,time,trackName):
        '''
        Add a track name event.
        '''
        pass
        
    def changeNoteTuning(self, tunings, sysExChannel=0x7F, realTime=False, tuningProgam=0):
        '''Change the tuning of MIDI notes
        '''
        pass
    
    def processEventList(self):
        '''
        Process the event list, creating a MIDIEventList
        
        For each item in the event list, one or more events in the MIDIEvent
        list are created.
        '''
        pass

    def removeDuplicates(self):
        '''
        Remove duplicates from the eventList.
        
        This function will remove duplicates from the eventList. This is necessary
        because we the MIDI event stream can become confused otherwise.
        '''
        pass


    def closeTrack(self):
        '''Called to close a track before writing
        
        This function should be called to "close a track," that is to
        prepare the actual data stream for writing. Duplicate events are
        removed from the eventList, and the MIDIEventList is created.
        
        Called by the parent MIDIFile object.
        '''
        pass
        
    def writeMIDIStream(self):
        '''
        Write the meta data and note data to the packed MIDI stream.
        '''
        pass

    def writeEventsToStream(self):
        '''
        Write the events in MIDIEvents to the MIDI stream.
        '''
        pass
        
    def deInterleaveNotes(self):
        '''Correct Interleaved notes.
        
        Because we are writing multiple notes in no particular order, we
        can have notes which are interleaved with respect to their start
        and stop times. This method will correct that. It expects that the
        MIDIEventList has been time-ordered.
        '''
        pass


    def adjustTime(self,origin):
        '''
        Adjust Times to be relative, and zero-origined
        '''
        pass
        
    def writeTrack(self,fileHandle):
        '''
        Write track to disk.
        '''
        pass


class MIDIHeader:
    '''
    Class to encapsulate the MIDI header structure.
    
    This class encapsulates a MIDI header structure. It isn't used for much,
    but it will create the appropriately packed identifier string that all
    MIDI files should contain. It is used by the MIDIFile class to create a
    complete and well formed MIDI pattern.
    
    '''
    def __init__(self,numTracks):
        ''' Initialize the data structures
        '''
        self.headerString = struct.pack('cccc',b'M',b'T',b'h',b'd')
        self.headerSize = struct.pack('>L',6)
        # Format 1 = multi-track file
        self.format = struct.pack('>H',1)
        self.numTracks = struct.pack('>H',numTracks)
        self.ticksPerBeat = struct.pack('>H',TICKSPERBEAT)
    

    def writeFile(self,fileHandle):
        pass

class MIDIFile:
    '''Class that represents a full, well-formed MIDI pattern.
    
    This is a container object that contains a header, one or more tracks,
    and the data associated with a proper and well-formed MIDI pattern.
    
    Calling:
    
        MyMIDI = MidiFile(tracks, removeDuplicates=True,  deinterleave=True)
        
        normally
        
        MyMIDI = MidiFile(tracks)
        
    Arguments:
    
        tracks: The number of tracks this object contains
            
        removeDuplicates: If true (the default), the software will remove duplicate
        events which have been added. For example, two notes at the same channel,
        time, pitch, and duration would be considered duplicate.
        
        deinterleave: If True (the default), overlapping notes (same pitch, same
        channel) will be modified so that they do not overlap. Otherwise the sequencing
        software will need to figure out how to interpret NoteOff events upon playback.
    '''
    
    def __init__(self, numTracks, removeDuplicates=True,  deinterleave=True):
        '''
        Initialize the class
        '''
        self.header = MIDIHeader(numTracks)
        
        self.tracks = list()
        self.numTracks = numTracks
        self.closed = False
        
        for i in range(0,numTracks):
            self.tracks.append(MIDITrack(removeDuplicates,  deinterleave))
            
            
    # Public Functions. These (for the most part) wrap the MIDITrack functions, where most
    # Processing takes place.
    
    def addNote(self,track, channel, pitch,time,duration,volume):
        """
        Add notes to the MIDIFile object
        
        Use:
            MyMIDI.addNotes(track,channel,pitch,time, duration, volume)
            
        Arguments:
            track: The track to which the note is added.
            channel: the MIDI channel to assign to the note. [Integer, 0-15]
            pitch: the MIDI pitch number [Integer, 0-127].
            time: the time (in beats) at which the note sounds [Float].
            duration: the duration of the note (in beats) [Float].
            volume: the volume (velocity) of the note. [Integer, 0-127].
        """
        pass

    def addTrackName(self,track, time,trackName):
        """
        Add a track name to a MIDI track.
        
        Use:
            MyMIDI.addTrackName(track,time,trackName)
            
        Argument:
            track: The track to which the name is added. [Integer, 0-127].
            time: The time at which the track name is added, in beats [Float].
            trackName: The track name. [String].
        """
        pass
        
    def addTempo(self,track, time,tempo):
        """
        Add a tempo event.
        
        Use:
            MyMIDI.addTempo(track, time, tempo)
            
        Arguments:
            track: The track to which the event is added. [Integer, 0-127].
            time: The time at which the event is added, in beats. [Float].
            tempo: The tempo, in Beats per Minute. [Integer]
        """
        pass
        
    def addProgramChange(self,track, channel, time, program):
        """
        Add a MIDI program change event.
        
        Use:
            MyMIDI.addProgramChange(track,channel, time, program)
            
        Arguments:
            track: The track to which the event is added. [Integer, 0-127].
            channel: The channel the event is assigned to. [Integer, 0-15].
            time: The time at which the event is added, in beats. [Float].
            program: the program number. [Integer, 0-127].
        """
        pass
    
    def addControllerEvent(self,track, channel,time,eventType, paramerter1):
        """
        Add a MIDI controller event.
        
        Use:
            MyMIDI.addControllerEvent(track, channel, time, eventType, parameter1)
            
        Arguments:
            track: The track to which the event is added. [Integer, 0-127].
            channel: The channel the event is assigned to. [Integer, 0-15].
            time: The time at which the event is added, in beats. [Float].
            eventType: the controller event type.
            parameter1: The event's parameter. The meaning of which varies by event type.
        """
        pass
        
    def changeNoteTuning(self,  track,  tunings,   sysExChannel=0x7F,  \
                         realTime=False,  tuningProgam=0):
        """
        Change a note's tuning using SysEx change tuning program.
            
        Use:
            MyMIDI.changeNoteTuning(track,[tunings],realTime=False, tuningProgram=0)
            
        Arguments:
            track: The track to which the event is added. [Integer, 0-127].
            tunings: A list of tuples in the form (pitchNumber, frequency). 
                     [[(Integer,Float]]
            realTime: Boolean which sets the real-time flag. Defaults to false.
            sysExChannel: do note use (see below).
            tuningProgram: Tuning program to assign. Defaults to zero. [Integer, 0-127]
            
        In general the sysExChannel should not be changed (parameter will be depreciated).
        
        Also note that many software packages and hardware packages do not implement
        this standard!
        """
        pass
  
    def writeFile(self,fileHandle):
        '''
        Write the MIDI File.
        
        Use:
            MyMIDI.writeFile(filehandle)
        
        Arguments:
            filehandle: a file handle that has been opened for binary writing.
        '''
        pass

    def addSysEx(self,track, time, manID, payload):
        """
        Add a SysEx event
        
        Use:
            MyMIDI.addSysEx(track,time,ID,payload)
            
        Arguments:
            track: The track to which the event is added. [Integer, 0-127].
            time: The time at which the event is added, in beats. [Float].
            ID: The SysEx ID number
            payload: the event payload.
            
        Note: This is a low-level MIDI function, so care must be used in
        constructing the payload. It is recommended that higher-level helper
        functions be written to wrap this function and construct the payload if
        a developer finds him or herself using the function heavily.
        """
        pass
    
    def addUniversalSysEx(self,track,  time,code, subcode, payload,  \
                          sysExChannel=0x7F,  realTime=False):
        """
        Add a Universal SysEx event.
        
        Use:
            MyMIDI.addUniversalSysEx(track, time, code, subcode, payload,\
                                      sysExChannel=0x7f, realTime=False)
                    
        Arguments:
            track: The track to which the event is added. [Integer, 0-127].
            time: The time at which the event is added, in beats. [Float].
            code: The even code. [Integer]
            subcode The event sub-code [Integer]
            payload: The event payload. [Binary string]
            sysExChannel: The SysEx channel.
            realTime: Sets the real-time flag. Defaults to zero.
        
        Note: This is a low-level MIDI function, so care must be used in
        constructing the payload. It is recommended that higher-level helper
        functions be written to wrap this function and construct the payload if
        a developer finds him or herself using the function heavily. As an example
        of such a helper function, see the changeNoteTuning function, both here and
        in MIDITrack.
        """
        pass
                                               
    def shiftTracks(self,  offset=0):
        """Shift tracks to be zero-origined, or origined at offset.
        
        Note that the shifting of the time in the tracks uses the MIDIEventList -- in other
        words it is assumed to be called in the stage where the MIDIEventList has been
        created. This function, however, it meant to operate on the eventList itself.
        """
        pass

    #End Public Functions ########################
    
    def close(self):
        '''Close the MIDIFile for further writing.
        
        To close the File for events, we must close the tracks, adjust the time to be
        zero-origined, and have the tracks write to their MIDI Stream data structure.
        '''
        pass
    
    
    def findOrigin(self):
        '''Find the earliest time in the file's tracks.append.
        '''
        pass
            
def writeVarLength(i):
    '''Accept an input, and write a MIDI-compatible variable length stream
    
    The MIDI format is a little strange, and makes use of so-called variable
    length quantities. These quantities are a stream of bytes. If the most
    significant bit is 1, then more bytes follow. If it is zero, then the
    byte in question is the last in the stream
    '''
    pass

def frequencyTransform(freq):
    '''Returns a three-byte transform of a frequencyTransform
    '''
    pass
    
def returnFrequency(freqBytes):
    '''The reverse of frequencyTransform. Given a byte stream, return a frequency.
    '''
    pass
