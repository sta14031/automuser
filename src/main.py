# https://github.com/wybiral/python-musical
from musical.theory import Note, Scale, Chord
from musical.audio import playback
from timeline import Hit, Timeline

from itertools import zip_longest
from random import uniform

from random_progression import *
from random_rhythm import *
from random_melody import *

# Define key and scale
key = Note('C4')
#scale = Scale(key, uniform(0, 1) > 0.5 and 'major' or 'minor')
scale = Scale(key, 'major')

# Grab key_chords chords from scale starting at the octave of our key
key_chords = Chord.progression(scale, base_octave=key.octave)

time = 0.0 # Keep track of currect note placement time in seconds
rhythm_mod = uniform(0.5, 1.5) # lower number = faster tempo

timeline = Timeline()

def render_melody(rhythm, melody):
    global time
    for r, m in zip(rhythm, melody):
        # print("len(chords) = %s, m = %s" %(len(key_chords), m))
        note = key_chords[m]
        timeline.add(time, Hit(note.notes[0], rhythm_mod * r / 2.0))
        time += rhythm_mod * r / 2.0

def render_progression(progression):
    global time
    for i, p in enumerate(progression):
        chord = key_chords[p]
        root, third, fifth = chord.notes

        timeline.add(time + i * 2 * rhythm_mod, Hit( root, 2 * rhythm_mod))
        timeline.add(time + i * 2 * rhythm_mod, Hit(fifth, 2 * rhythm_mod))

def DEPRECATED_add_song_part(progression, rhythm, melody):
    global time
    for pI, mI in zip_longest(progression, melody):
        chord = key_chords[pI or 0]
        note = key_chords[mI or 0]
        root, third, fifth = chord.notes
        # arpeggio = [root, third, fifth, third, root, third, fifth, third]
        # for i, interval in enumerate(arpeggio):
        #     ts = float(i * 2) / len(arpeggio)
        #     timeline.add(time + ts, Hit(interval, 1.0))
        timeline.add(time, Hit(root,  rhythm_mod - 0.2))
        timeline.add(time, Hit(fifth, rhythm_mod - 0.2))

        # Add the melody note
        timeline.add(time, Hit(note.notes[0], rhythm_mod / 2 - 0.2))
        timeline.add(time + rhythm_mod / 2, Hit(note.notes[1], rhythm_mod / 2 - 0.2))
        time += rhythm_mod

# Add key_chords to timeline by arpeggiating chords from the key_chords
# Instead of arpeggiating, just do the base chords
# progression = make_progression_part()
# melody = make_melody_part(0)

# Come up with two progressions and use them smartly, use melodies in conjunction
progression1 = make_progression_part()
progression2 = make_progression_part()
rhythm1 = make_rhythm_part()
rhythm2 = make_rhythm_part()
melody1 = make_melody_part(len(rhythm1))
melody2 = make_melody_part(len(rhythm2))

# DEPRECATED_add_song_part(progression1, rhythm1, melody1)
# DEPRECATED_add_song_part(progression1, rhythm1, melody1)
# DEPRECATED_add_song_part(progression2, rhythm2, melody2)
# DEPRECATED_add_song_part(progression1, rhythm1, melody1)
render_progression(progression1)
render_melody(rhythm1, melody1)
render_progression(progression1)
render_melody(rhythm1, melody1)
render_progression(progression2)
render_melody(rhythm2, melody2)
render_progression(progression1)
render_melody(rhythm1, melody1)

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
