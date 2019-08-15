#!/usr/bin/env python

import soundfile as sf
import math

sampleRate = 44100
breakpoint = 19632
dropout = 1937

def generate(f):
    with sf.SoundFile("./audio.wav", mode="x", samplerate=44100, channels=1, subtype="PCM_24") as file:
        for i in range(sampleRate):
            idx = i if i < breakpoint else i + dropout
            file.write(math.sin(idx * f * 2 * math.pi / sampleRate))

generate(100)
