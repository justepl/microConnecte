from pynput from keyboard
import time
import pyaudio
import wave


form_1 = pyaudio.paInt16  # 16-bit resolution
chans = 1  # 1 channel
samp_rate = 44100  # 44.1kHz sampling rate
chunk = 4096  # 2^12 sample for buffer
record_secs = 3  # sec to reccord
dev_index = 2  # device index found by p.get_device_info_by_index (2 pour l'instant)
wav_output_filename = 'test1.wav'  # output's file name

audio = pyaudio.PyAudio()  # audio obj from PyAudio class
frame = []

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

        self.stream = p.open(format=form_1,
                             channels = chans,
                             rate = samp_rate,
                             input = True,
                             frame_per_buffer = chunk,
                             stream_callback = self.callback)
        print self.stream.is_active()

    def on_press(self, key):
        if key == keyboard.Key.cmd_l:
            self.key_pressed = True

    def on_release(self, key):
        if key == keyboard.Key.cmd_l:
            self.key_pressed = False

    def callback(self, in_data, frame_count, time_info, status):
        if self.key_pressed == True:
            return (in_data, pyaudio.paContinue)
        elif self.key_pressed == False:
            return (in_data, pyaudio.paComplete)
        else:
            return (in_data, pyaudio.paAbort)

listener = MyListener()
listener.start()
started = False

while True:
    time.sleep(0.1)
    if listener.key_pressed == True and started == False:
        started = True
        listener.stream.start_stream()
        print("stream start")

    elif listener.key_pressed == False and started == True:
        print("bad")
        listener.stream.stop_stream()
        listener.stream.close()
        p.terminate()

        wf = wave.open(wav_output_filename, 'wb')
        wf.setnchannels(chans)
        wf.setsampwidth(p.get_sample_size(form_1))
        wf.setframerate(samp_rate)
        wf.writeframes(b''.join(frame))
        wf.close()

        started = False

# stream = audio.open(format=form_1, rate=samp_rate, channels=chans, input_device_index=dev_index, input=True,
#                     frames_per_buffer=chunk, stream_callback = self.callback)


