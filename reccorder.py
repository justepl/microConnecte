import pyaudio
import wave
import sys
from threading import Thread

form_1 = pyaudio.paInt16  # 16-bit resolution
chans = 1  # 1 channel
samp_rate = 44100  # 44.1kHz sampling rate
chunk = 4096  # 2^12 sample for buffer
record_secs = 3  # sec to reccord
dev_index = 2  # device index found by p.get_device_info_by_index (2 pour l'instant)
wav_output_filename = 'test1.wav'  # output's file name

audio = pyaudio.PyAudio()  # audio obj from PyAudio class

stream = audio.open(format=form_1, rate=samp_rate, channels=chans, input_device_index=dev_index, input=True,
                    frames_per_buffer=chunk)

state = "R"


class Reccorder(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while true:
            if state == "R":
                frames = []
                print("recording")
                while state == "R":
                    state = input("R reccord, S stop")
                    data = stream.read(chunk)
                    frames.append(data)

        if state == "S":
            print("finished recording")

            # stop the stream, close it and destroy audio
            stream.stop_stream()
            stream.close()
            audio.terminate()

            # save the audio frames as .wav file
            wavefile = wave.open(wav_output_filename, 'wb')
            wavefile.setnchannels(chans)
            wavefile.setsampwidth(audio.get_sample_size(form_1))
            wavefile.setframerate(samp_rate)
            wavefile.writeframes(b''.join(frames))
            wavefile.close()


class Listener(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while true:
            state = input("R reccord, S stop")
        print(state)


thread_Listen = Listener()
thread_Reccorder = Reccorder()

thread_Listen.start()
thread_Reccorder.start()

thread_Listen.join()
thread_Reccorder.join()
