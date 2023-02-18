from score import Score

score = Score()


def create_note_children_from_pattern(
    parent_diatonic_position, parent_note_duration, note_shift_pattern
):
    """Create a list of child notes from a parent note and a pattern of note shifts."""

    # the note plus the changes is the total number of children
    subdivisions = len(note_shift_pattern) + 1
    child_duration = parent_note_duration / subdivisions
    children_durations = [child_duration] * subdivisions
    # first note is always the original note
    first_child = parent_diatonic_position

    children_diatonic_positions = [first_child]
    net_shift = 0
    for shift in note_shift_pattern:
        net_shift = shift + net_shift
        children_diatonic_positions.append(parent_diatonic_position + net_shift)

    return children_diatonic_positions, children_durations


def create_children_of_notes_from_pattern(
    parent_diatonic_positions, parent_note_durations, note_shift_pattern
):
    all_children_diatonic_positions = []
    all_children_durations = []
    for i in range(len(parent_diatonic_positions)):
        parent_diatonic_position = parent_diatonic_positions[i]
        parent_note_duration = parent_note_durations[i]
        (
            children_diatonic_positions,
            children_durations,
        ) = create_note_children_from_pattern(
            parent_diatonic_position, parent_note_duration, note_shift_pattern
        )

        all_children_diatonic_positions = (
            all_children_diatonic_positions + children_diatonic_positions
        )
        all_children_durations = all_children_durations + children_durations
    print("all_children_diatonic_positions")
    print(all_children_diatonic_positions)
    print("all_children_durations")
    print(all_children_durations)
    return all_children_diatonic_positions, all_children_durations


note_shift_pattern = [1, 1]  # movements along the diatonic scale to create the pattern

parent_diatonic_position = 1
parent_note_duration = 4

fractal_dimensions = 6
parent_diatonic_positions = [parent_diatonic_position]
parent_note_durations = [parent_note_duration]
for i in range(fractal_dimensions):
    score.add_pitches_to_score(parent_diatonic_positions, parent_note_durations)

    (
        children_diatonic_positions,
        children_note_durations,
    ) = create_children_of_notes_from_pattern(
        parent_diatonic_positions, parent_note_durations, note_shift_pattern
    )

    parent_diatonic_positions = children_diatonic_positions
    parent_note_durations = children_note_durations

score.add_pitches_to_score(children_diatonic_positions, children_note_durations)

score.save_score("test.mid")
