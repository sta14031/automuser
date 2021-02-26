# https://github.com/wybiral/python-musical
from musical.theory import Note, Scale, Chord
from musical.audio import playback
from timeline import Hit, Timeline

from itertools import zip_longest

from random_progression import *
from random_melody import *

# Define key and scale
key = Note('A3')
scale = Scale(key, 'minor')

# Grab key_chords chords from scale starting at the octave of our key
key_chords = Chord.progression(scale, base_octave=key.octave)

time = 0.0 # Keep track of currect note placement time in seconds

timeline = Timeline()

# Add key_chords to timeline by arpeggiating chords from the key_chords
# Instead of arpeggiating, just do the base chords
progression = make_progression_part()
melody = make_melody_part(0)

print(melody)

for pI, mI in zip_longest(progression, melody):
    chord = key_chords[pI or 0]
    note = key_chords[mI or 0]
    root, third, fifth = chord.notes
    # arpeggio = [root, third, fifth, third, root, third, fifth, third]
    # for i, interval in enumerate(arpeggio):
    #     ts = float(i * 2) / len(arpeggio)
    #     timeline.add(time + ts, Hit(interval, 1.0))
    timeline.add(time, Hit(root,  1.8))
    timeline.add(time, Hit(fifth, 1.8))

    # Add the melody note
    timeline.add(time, Hit(note.notes[0], 0.5))
    timeline.add(time + 1.0, Hit(note.notes[1], 0.5))
    time += 2.0

# Strum out root chord to finish
chord = key_chords[0]
timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
timeline.add(time + 0.1, Hit(chord.notes[1], 4.0))
timeline.add(time + 0.2, Hit(chord.notes[2], 4.0))
timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 4.0))
timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 4.0))
timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 4.0))

print("Rendering audio...")

data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")

playback.play(data)

print("Done!")
