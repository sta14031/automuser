from random import uniform

# a very complicated thing that does cool music
freq_adjust_matrix = [
    [ 0,  3,  1,  5, -1, -1, -1],
    [-2,  0,  3,  6,  0, -3,  0],
    [ 2, -1,  0,  4, -1,  6,  1],
    [ 2,  3, -1,  0, 10,  2,  0],
    [ 4,  1,  2,  2,  0,  2,  3],
    [-3,  3,  4,  8,  1,  0,  5],
    [-1, -2,  3,  0,  3,  1,  0]
]

def make_progression_part():
    # A progression consists of between 4 and 8 chords.
    # We tend to resolve on tonic.

    notes = [] # The sequence of notes so far

    # Relative note frequencies
    freq = [8, 0, 0, 0, 0, 2, 0]
    while (True):
        # Select a new chord.
        target = uniform(0, sum(freq))
        i = -1
        v = 0
        while v < target:
            i += 1
            v += freq[i]

        # Now our new chord index (i) has been selected
        notes.append(i)
        freq[i] = 0 # can't have the same chord twice

        #if i == 4 and uniform(0, 1) > 0.5:
        if len(notes) == 4:
            # End the progression here
            # notes.append(0)
            break

        # apply the cool matrix
        freq = [f + m for f, m in zip(freq, freq_adjust_matrix[i])]

        freq = [f if f > 0 else 0 for f in freq] # can't have negative frequencies

    #print(notes)
    return notes

def make_progression_ending():
    return [3, 4, 0]