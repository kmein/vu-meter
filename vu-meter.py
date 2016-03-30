#!/usr/bin/python3
import pyaudio
from amplitude import Amplitude

RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

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
