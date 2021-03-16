from random import uniform
import math

# a complicated thing that does cool music
freq_adjust_matrix = [
    [ 0,  3,  1,  0],
    [ 4,  3,  0,  1],
    [ 2,  5, -6,  1],
    [ 2, -3, -3, -9]
]

conversions= [1, 2, 4]

def make_melody_part(num_notes):
    # Melodies can go up by 2nds, 3rds, or 5ths.
    # We tend to resolve on tonic.

    notes = [] # The sequence of notes so far

    # Relative note frequencies: 2nd, 3rd, 5th, other.
    freq = [8, 2, 1, 0]
    while (True):
        # Select a new chord.
        target = uniform(0, sum(freq))
        i = -1
        v = 0
        while v < target:
            i += 1
            v += freq[i]

        # Now our new melody index (i) has been selected
        notes.append(((len(notes) == 0) and 1 or notes[-1])
            + (i == 3 and uniform(0, 6) or conversions[i])
            * (uniform(0, 1) > 0.5 and 1 or -1))
        freq[i] = 0 # can't have the same note twice TODO: can we?

        #if i == 0 and len(notes) >= 4 and uniform(0, 1) > 0.5: #TODO: uniform -> random_int
        if len(notes) == num_notes:
            # End the progression here
            # notes.append(0)
            break

        # apply the cool matrix
        freq = [f + m for f, m in zip(freq, freq_adjust_matrix[i])]

        freq = [f if f > 0 else 0 for f in freq] # can't have negative frequencies

    print(notes)
    adjusted_notes = [n - 7 if n >= 7 else n for n in [abs(math.floor(n)) for n in notes]]
    return adjusted_notes