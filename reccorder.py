import pyaudio
import wave
import threading
import multiprocessing

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

continuOrNot = multiprocessing.Queue()

frames = []


def reccord():
    # if streamBool:

    # while True:
    if streamChar == "R":
        # loop through stream and append audio chunks to frame array
        data = stream.read(chunk)
        frames.append(data)

    elif streamChar == "S":
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


def keyboardInput():
    # while True:
    try :
        inputVar = input("R for reccord S for Stop")
    except:
        inputVar = "a"
    continuOrNot.put(inputVar)

if __name__=="__main__":
    processes = [multiprocessing.Process(target=keyboardInput),
             multiprocessing.Process(target=reccord)]

    for p in processes:
        p.start()

    # if __name__ == '__main__':

    # worker_qui_met_a_jour_les_flux = Process(target=mettre_a_jour_les_flux,
    #                                          args=(queue_de_flux_a_mettre_a_jour,
    #                                                queue_de_mises_a_jour_des_flux))
    #
    # worker_qui_demande_la_mise_a_jour = Process(target=demander_la_mise_a_jour_des_flux,
    #                                             args=(queue_de_flux_a_mettre_a_jour,
    #                                                   flux_rss))
