import numpy as np


class Generator:
    """Tool to generate a fractal pattern of notes of appropriate durations"""

    def __init__(self):
        pass

    def get_shift_pattern_from_notes(self, notes):
        """Convert a list of notes to a list of shifts."""
        note_shift_pattern = []
        for i in range(len(notes) - 1):
            note_shift_pattern.append(notes[i + 1] - notes[i])
        return note_shift_pattern

    def create_note_children_from_pattern(
        self, parent_diatonic_position, parent_note_duration, note_shift_pattern
    ):
        """Create a list of child notes from a parent note and a pattern of note
        shifts."""

        # the note plus the changes is the total number of children
        subdivisions = len(note_shift_pattern) + 1
        child_duration = parent_note_duration / subdivisions
        children_durations = [child_duration] * subdivisions

        # first note is always the original note
        first_child = parent_diatonic_position

        children_diatonic_positions = [first_child]
        net_shift = 0
        for shift in note_shift_pattern:
            if np.isnan(shift):  # nan indicates silence:
                # add a silence
                children_diatonic_positions.append(np.nan)
            else:
                net_shift = shift + net_shift
                children_diatonic_positions.append(parent_diatonic_position + net_shift)

        return children_diatonic_positions, children_durations

    def create_children_of_notes_from_pattern(
        self, parent_diatonic_positions, parent_note_durations, note_shift_pattern
    ):
        """Create a list of child notes from a list of parent notes and a pattern of
        note"""

        all_children_diatonic_positions = []
        all_children_durations = []
        for i in range(len(parent_diatonic_positions)):
            parent_diatonic_position = parent_diatonic_positions[i]
            parent_note_duration = parent_note_durations[i]
            (
                children_diatonic_positions,
                children_durations,
            ) = self.create_note_children_from_pattern(
                parent_diatonic_position, parent_note_duration, note_shift_pattern
            )

            all_children_diatonic_positions = (
                all_children_diatonic_positions + children_diatonic_positions
            )
            all_children_durations = all_children_durations + children_durations

        return all_children_diatonic_positions, all_children_durations

    def create_fractal_notes(
        self,
        fractal_dimensions,
        measure_duration,
        multiplier_on_pattern_at_each_dimension,
        note_shift_pattern_at_each_dimension,
    ):
        """Return a list of notes and durations for each fractal dimension."""

        # just the number of notes to move off from middle c at the beginning
        # everything stems from the tonic. Also, the measure duration is just the
        # original duration before fractal patterns are applied
        parent_diatonic_positions = [1]
        parent_note_durations = [measure_duration]

        pitches_at_dimension = []
        durations_at_dimension = []
        for i in range(fractal_dimensions + 1):
            (
                children_diatonic_positions,
                children_note_durations,
            ) = self.create_children_of_notes_from_pattern(
                parent_diatonic_positions,
                parent_note_durations,
                np.array(note_shift_pattern_at_each_dimension[i])
                * multiplier_on_pattern_at_each_dimension[i],
            )

            pitches_at_dimension.append(children_diatonic_positions)
            durations_at_dimension.append(children_note_durations)

            # recursive where the magic happens!!! :D
            parent_diatonic_positions = children_diatonic_positions
            parent_note_durations = children_note_durations

        return pitches_at_dimension, durations_at_dimension
