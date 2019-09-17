#!/usr/bin/env python


import soundfile as sf
import sys


class MovingAvg():
	def __init__(self, size):
		self.size = size
		self.clear()
		
	def clear(self):
		self.values = []
		self.avg = 0.0

	def add(self, v):
		self.avg += (v * 1.0 / self.size)
		self.values.append(v)
		if (len(self.values) > self.size):
			p = self.values.pop(0)
			self.avg -= (p * 1.0 / self.size)

	def first(self):
		return self.values[0]

	def value(self):
		return self.avg if (len(self.values) == self.size) else (self.avg * self.size / len(self.values))




avg5 = MovingAvg(5)
data, samplerate = sf.read(sys.argv[1])


discontinuities = []


for i in range(len(data)):
    d = data[i]
    if len(avg5.values) == avg5.size:
        a = avg5.value()
        c = abs(d - a)
        if c > 0.2:
            discontinuities.append(i)
            print("abnormal change found from %d to %d (%.6f to %.6f) avg %.6f change %.6f" % (i - 1, i, data[i - 1], d, a, c))            
            avg5 = MovingAvg(5)
        else:
            avg5.add(d)
    else:
        avg5.add(d)
    
avgLen = 20
for d in discontinuities:
    avg20 = MovingAvg(avgLen)
    for i in range(d - (2 * avgLen), d + (2 * avgLen)):
        avg20.add(data[i])
        if i > (d - avgLen) and i < (d + avgLen):
            f = (d - i) / (1.0 * avgLen)
            data[i] = ((1.0 - abs(f)) * avg20.value()) + (abs(f) * data[i])

sf.write("./fixed.wav", data, samplerate)

