import numpy as np
from midiutil.MidiFile import MIDIFile

MAJOR_SCALE_SHIFTS_CUMULATIVE = np.cumsum([2, 2, 1, 2, 2, 2, 1])
MINOR_SCALE_SHIFTS_CUMULATIVE = np.cumsum([2, 1, 2, 2, 1, 2, 2])
OCTAVES = 9  # possible range

# add an offset to account for the negative diatonic positions not wrapping
# the notes_in_key array
OFFSET = 12 * 2
BASE_PITCH = 60 - OFFSET
MINOR_SCALE = [BASE_PITCH]
MAJOR_SCALE = [BASE_PITCH]
for i in range(OCTAVES):
    for shift in MINOR_SCALE_SHIFTS_CUMULATIVE:
        octave_shift = i * 12
        MINOR_SCALE.append(BASE_PITCH + shift + octave_shift)

for i in range(OCTAVES):
    for shift in MAJOR_SCALE_SHIFTS_CUMULATIVE:
        octave_shift = i * 12
        MAJOR_SCALE.append(BASE_PITCH + shift + octave_shift)


class Score:
    """The object which we use to store our note and duration data"""

    def __init__(self):
        """initialize a simple midi track"""

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

    def set_key(self, key):
        """set the key to major or minor diatonic scale"""
        if key == "minor":
            self.notes_in_key = MINOR_SCALE
            return
        elif key == "major":
            self.notes_in_key = MAJOR_SCALE
            return
        assert False, 'ERROR: key must be either "major" or "minor"'

    def add_pitch_to_midifile(self, pitch, note_duration):
        """Add a pitch to the midifile."""
        self.mf.addNote(
            self.track, self.channel, pitch, self.time, note_duration, self.volume
        )

    def add_pitch_to_score(self, diatonic_position, note_duration):
        """Add a pitch to the score."""
        if not np.isnan(diatonic_position):
            pitch = self.notes_in_key[diatonic_position + OFFSET]
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

    def create_score(
        self,
        key,
        tempo_multiplier_over_time,
        fractal_dimensions_to_add,
        pitches_at_dimension,
        durations_at_dimension,
        filename,
    ):
        """Create a score by concatenating measures with one measure at a given
        fractal dimension"""

        self.set_key(key)
        for i in range(len(fractal_dimensions_to_add)):
            fractal_dimension = fractal_dimensions_to_add[i]
            duration_multiplier = 1 / tempo_multiplier_over_time[i]
            self.add_pitches_to_score(
                pitches_at_dimension[fractal_dimension],
                duration_multiplier
                * np.array(durations_at_dimension[fractal_dimension]),
            )

        self.save_score(filename)
