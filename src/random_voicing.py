from random import choice
import math

possible_voicings = [0, 1, 2]

def make_voicing_part(num_chords):
    # Returns a sequence of voicings for the chords.
    # The order of voicings does not really matter
    # so we just do it randomly.

    voicings = [] # The sequence of voicings so far

    for _ in range(num_chords):
        voicings.append([
            choice(possible_voicings),
            choice(possible_voicings)])

    return voicings