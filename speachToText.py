import vosk
import sys
import sounddevice as sd
import queue

model = vosk.Model('models_stt/vosk-model-uk-v3')
samplerate = 16000
device = 1

q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16', channels=1,
                       callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            print(rec.Result())
