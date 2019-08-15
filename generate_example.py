#!/usr/bin/env python

import soundfile as sf
import math

sampleRate = 44100

def generate(f):
    with sf.SoundFile("./audio.wav", mode="x", samplerate=44100, channels=1, subtype="PCM_24") as file:
        for i in range(sampleRate):
            file.write(math.sin(i * f * 2 * math.pi / sampleRate))

generate(1)
