import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt
CHANNELS = 1
RATE = 44100
SHIFT = 2


def callback(in_data, frame_count, time_info, flag):
    a = np.fromstring(in_data, np.float32)
    dfft = np.fft.rfft(a)
    dfft = np.roll(dfft, SHIFT)
    dfft[:SHIFT] = 0
    out_data = np.fft.irfft(dfft)*0.5
    out_data = out_data.astype(np.float32).tostring()
    return out_data, pyaudio.paContinue


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    pyaudio.paInputOverflow = 2
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    output_device_index=2,
                    stream_callback=callback)

    stream.start_stream()
    while stream.is_active():
        time.sleep(5)
    stream.stop_stream()
    stream.close()
    p.terminate()
