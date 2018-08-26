import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
SHIFT = 5

def callback(in_data, frame_count, time_info, flag):
    a = np.fromstring(in_data, np.float32)
    dfft = np.fft.rfft(a)
    #plt.plot(dfft)
    dfft = np.roll(dfft, SHIFT)
    dfft[-SHIFT:] = 0
    out_data = np.fft.irfft(dfft)
    print(type(out_data))
    print(out_data)
    out_data = out_data.astype(np.float32).tostring()
    print(frame_count)
    return out_data, pyaudio.paContinue


stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()
while stream.is_active():
    pass
time.sleep(10)
stream.stop_stream()
stream.close()
p.terminate()
