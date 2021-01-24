# https://github.com/wybiral/python-musical
from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

from random_progression import *

# Define key and scale
key = Note('D3')
scale = Scale(key, 'major')

# Grab key_chords chords from scale starting at the octave of our key
key_chords = Chord.progression(scale, base_octave=key.octave)

time = 0.0 # Keep track of currect note placement time in seconds

timeline = Timeline()

# Add key_chords to timeline by arpeggiating chords from the key_chords
progression = make_progression_part()
for index in progression:
    chord = key_chords[index]
    root, third, fifth = chord.notes
    arpeggio = [root, third, fifth, third, root, third, fifth, third]
    for i, interval in enumerate(arpeggio):
        ts = float(i * 2) / len(arpeggio)
        timeline.add(time + ts, Hit(interval, 1.0))
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
