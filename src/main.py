# https://github.com/wybiral/python-musical
from musical.theory import Note, Scale, Chord
from musical.theory.scale import NAMED_SCALES
from musical.audio import playback, save
from timeline import Hit, Timeline

from itertools import zip_longest
from random import uniform, randint, choice, seed
from sys import argv

from random_progression import *
from random_rhythm import *
from random_melody import *

# Set random seed + filepath from command line
random_seed = "0"
if len(argv) >= 2:
    random_seed = argv[1]
seed(random_seed)

filepath = "public/generated_songs/song_" + random_seed + ".wav"
if len(argv) > 2:
    filepath = argv[2]

# Define key and scale
random_note = choice(Note.NOTES)
key = Note(random_note + '3')
# scale = Scale(key, choice([l for l in list(NAMED_SCALES.values()) if len(l) == 7]))
scale = Scale(key, uniform(0, 1) > 0.3 and 'major' or 'minor')

# Grab key_chords chords from scale starting at the octave of our key
key_chords = Chord.progression(scale, base_octave=key.octave)

time = 0.0 # Keep track of currect note placement time in seconds
rhythm_mod = uniform(0.5, 1.5) # lower number = faster tempo
print("rhythm_mod = " + str(rhythm_mod))

timeline = Timeline()

def render_melody(rhythm, melody):
    global time

    print("r = " + str(rhythm))
    for r, m in zip(rhythm, melody):
        # print("len(chords) = %s, m = %s" %(len(key_chords), m))
        note = key_chords[m]
        timeline.add(time, Hit(note.notes[0], r * 2.0 * rhythm_mod))
        time += (r * 2.0 * rhythm_mod)

def render_progression(progression):
    global time
    for i, p in enumerate(progression):
        chord = key_chords[p]
        root, third, fifth = chord.notes

        timeline.add(time + i * 2.0 * rhythm_mod, Hit( root, 2.0 * rhythm_mod))
        timeline.add(time + i * 2.0 * rhythm_mod, Hit(fifth, 2.0 * rhythm_mod))

# Come up with several progressions, rhythms, and melodies
progressions = []
rhythms = []
melodies = []

complexity = randint(2, 5) # the length of the above arrays
for _ in range(complexity):
    progressions.append(make_progression_part())
    rhythms.append(make_rhythm_part())
    melodies.append(make_melody_part(len(rhythms[-1])))

# Render the progressions and melodies in patterns
song_length = randint(2, 3) * complexity // 2
for _ in range(song_length):
    render_progression(choice(progressions))
    i = randint(0, complexity - 1)
    render_melody(rhythms[i], melodies[i])

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

#print("Playing audio...")
print("Saving audio to " + filepath)

# Don't have to worry about running out of filespace because Heroku regularly refreshes the filesystem. See https://stackoverflow.com/questions/46282883/what-happens-to-temp-files-in-heroku-node-application
save.save_wave(data, filepath)
# playback.play(data)

print("Done!")
