from random import uniform

# a very complicated thing that does cool music
freq_adjust_matrix = [
#    2.0 1.5 1.0 0.5 0.25
   [-9, -9,  2,  2,  0],
    [0, -9, -3,  2,  0],
    [4,  1, -9,  4,  1],
    [0,  1,  2, -1,  4],
    [0,  0,  2,  4, -1],
]

delay_key = [2.0, 1.5, 1.0, 0.5, 0.25]

def make_rhythm_part():
    # A rhythm is a series of time delays applied to the melody.

    delays = [] # The sequence of delays so far
    final_delays = [] # Variable used for final adjustments

    # Relative time delay frequencies
    freq = [1, 0, 3, 2, 0]
    while (True):
        # Select a new delay.
        target = uniform(0, sum(freq))
        i = -1
        v = 0
        while v < target:
            i += 1
            v += freq[i]

        # Now our new rhythm index (i) has been selected
        delays.append(i)

        freq[i] -= 3 # reduce current rhythm frequency

        #if i == 4 and uniform(0, 1) > 0.5:
        if sum([delay_key[j] for j in delays]) >= 4.0:
            # End the rhythm here
            final_delays = [delay_key[j] for j in delays]
            while sum(final_delays) > 4.0:
                final_delays[-1] -= 0.25

            break

        # apply the cool matrix
        freq = [f + m for f, m in zip(freq, freq_adjust_matrix[i])]

        freq = [f if f > 0 else 0 for f in freq] # can't have negative frequencies

    # print(sum(final_delays))
    return final_delays