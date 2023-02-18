from midiutil.MidiFile import MIDIFile

MINOR_SCALE = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
MAJOR_SCALE = [60, 62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 84]


class Score:
    def __init__(self):
        # create your MIDI object
        self.mf = MIDIFile(1)  # only 1 track
        self.track = 0  # the only track

        self.time = 0  # start at the beginning
        self.mf.addTrackName(self.track, self.time, "Sample Track")
        self.mf.addTempo(self.track, self.time, 120)

        # add some notes
        self.channel = 0
        self.volume = 100

        self.time = 0  # start on beat 0

    def add_pitch_to_midifile(self, pitch, note_duration):
        """Add a pitch to the midifile."""
        self.mf.addNote(
            self.track, self.channel, pitch, self.time, note_duration, self.volume
        )

    def add_pitch_to_score(self, diatonic_position, note_duration):
        """Add a pitch to the score."""
        pitch = MAJOR_SCALE[diatonic_position]
        self.add_pitch_to_midifile(pitch, note_duration)
        self.time += note_duration

    def add_pitches_to_score(self, diatonic_positions, note_durations):
        """Add a list of pitches to the score."""
        for i in range(len(diatonic_positions)):
            diatonic_position = diatonic_positions[i]
            note_duration = note_durations[i]
            self.add_pitch_to_score(diatonic_position, note_duration)

    def save_score(self, name):
        """write it to disk"""
        with open(name, "wb") as outf:
            self.mf.writeFile(outf)
