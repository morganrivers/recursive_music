from generator import Generator
from score import Score

OCTAVE_NOTES = 8


def oct_d(note):
    return note - OCTAVE_NOTES + 1


def oct_dd(note):
    return note - 2 * OCTAVE_NOTES + 1


def oct_u(note):
    return note + OCTAVE_NOTES - 1


def oct_uu(note):
    return note - 2 * OCTAVE_NOTES - 1


generator = Generator()

# 1 being C, 2 being D, etc, in a C major (or minor) scale
# (actual pitches don't match that scale though.
# for example, [1, 2, 3, 4, 5, 6, 7, oct_u(1)] would be an ascending major scale
notes_to_pattern_from_first_fractal_dimension = [1, 6, 5]

key = "major"

note_shift_pattern_dim_1 = generator.get_shift_pattern_from_notes(
    notes_to_pattern_from_first_fractal_dimension
)

note_shift_patterns_at_each_dimension = [
    note_shift_pattern_dim_1,
    note_shift_pattern_dim_1,
    note_shift_pattern_dim_1,
    note_shift_pattern_dim_1,
]
multiplier_on_pattern_at_each_dimension = [1, 1, 1, 1]

fractal_dimensions_to_play_over_time = [1, 1, 1, 2, 3, 3, 2, 2, 1, 1]
tempo_multiplier_over_time = [4, 4, 4, 3, 1, 1, 3, 2.5, 4, 3]
measure_duration = 16

score = Score()

fractal_dimensions_to_compute = max(fractal_dimensions_to_play_over_time)

pitches_at_dimension, durations_at_dimension = generator.create_fractal_notes(
    fractal_dimensions_to_compute,
    measure_duration,
    multiplier_on_pattern_at_each_dimension,
    note_shift_patterns_at_each_dimension,
)

filename = "test.mid"

score.create_score(
    key,
    tempo_multiplier_over_time,
    fractal_dimensions_to_play_over_time,
    pitches_at_dimension,
    durations_at_dimension,
    filename,
)
