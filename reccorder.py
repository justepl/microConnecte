import pyaudio
import wave
import threading
from multiprocessing import Process, Queue, TimeoutError
import sys
import time

form_1 = pyaudio.paInt16  # 16-bit resolution
chans = 1  # 1 channel
samp_rate = 44100  # 44.1kHz sampling rate
chunk = 4096  # 2^12 samples for buffer
record_secs = 3  # seconds to record
dev_index = 2  # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav'  # name of .wav file

audio = pyaudio.PyAudio()  # create pyaudio instantiation

streamChar = "a"

# create pyaudio stream
stream = audio.open(format=form_1, rate=samp_rate, channels=chans,
                    input_device_index=dev_index, input=True,
                    frames_per_buffer=chunk)

continuOrNot = Queue()

frames = []

inputVar = "a"


class Reccorder():

    def reccord(self):
        # if streamBool:
        print("func Reccord")
        # while True:
        # inputVar = continuOrNot.get()
        global inputVar
        if inputVar == "R":
            # loop through stream and append audio chunks to frame array
            print("reccord")
            data = stream.read(chunk)
            frames.append(data)

        elif inputVar == "S":
            print("finished recording")

            # stop the stream, close it, and terminate the pyaudio instantiation
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

    def keyboardInput(self):
        global inputVar
        # inputVar = "a"
        print("inputVar :", inputVar)
        while inputVar != "R" or inputVar != "S":
            print("inputVar :", inputVar)

            time.sleep(3)
            # try:
            print("try")
            print("R for reccord S for Stop \n")
            inputVar = eval(input())
            while inputVar != "R" or inputVar != "S":
                inputVar = eval(input())

            # inputVar.rstrip()

            continuOrNot.put(inputVar)
            print("queu : ", continuOrNot)
            inputVar = "a"


# except:
#     inputVar = "a"


if __name__ == "__main__":
    reccorderInstance = Reccorder()

    worker1 = Process(target=reccorderInstance.reccord, args=())
    worker2 = Process(target=reccorderInstance.keyboardInput, args=())
    i = 0
    while i <= 2:
        worker2.start()
        worker1.start()

        worker1.join()
        worker2.join()
        i = i + 1
