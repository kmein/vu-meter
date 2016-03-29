#!/usr/bin/python3
import math
import struct
import pyaudio

SHORT_NORMALIZE = 1.0 / 32768.0
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

class Amplitude:
    ''' an abstraction for Amplitudes (with an underlying float value)
    that packages a display function and many more '''

    def __init__(self, value=0):
        self.value = value

    def __add__(self, other):
        return Amplitude(self.value + other.value)

    def __sub__(self, other):
        return Amplitude(self.value - other.value)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def to_int(self, scale=1):
        ''' convert an amplitude to an integer given a scale such that one can
        choose the precision of the resulting integer '''

        return int(self.value * scale)

    @staticmethod
    def from_block(block):
        ''' generate an Amplitude object based on a block of audio input data '''
        count = len(block) / 2
        shorts = struct.unpack("%dh" % count, block)
        sum_squares = sum(s**2 * SHORT_NORMALIZE**2 for s in shorts)
        return Amplitude(math.sqrt(sum_squares / count))

    def display(self, mark, scale=50):
        ''' display an amplitude and another (marked) maximal Amplitude
        graphically '''
        int_val = self.to_int(scale)
        mark_val = mark.to_int(scale)
        delta = abs(int_val - mark_val)
        print(int_val * '*', (delta-1) * ' ', '|')

def main():
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=INPUT_FRAMES_PER_BLOCK
                           )

        maximal = Amplitude()
        while True:
            data = stream.read(INPUT_FRAMES_PER_BLOCK)
            amp = Amplitude.from_block(data)
            if amp > maximal:
                maximal = amp
            amp.display(scale=100, mark=maximal)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
