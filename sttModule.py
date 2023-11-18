import vosk
import sys
import sounddevice as sd
import queue
import json

q = queue.Queue()


def query_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def listen(callback, stt_model, assistant_alias, assistant_cmd_list):
    model = stt_model['model']
    sample_rate = stt_model['sample_rate']
    block_size = stt_model['block_size']
    device = stt_model['device']
    d_type = stt_model['d_type']
    channels = stt_model['channels']

    with sd.RawInputStream(samplerate=sample_rate, blocksize=block_size, device=device, dtype=d_type, channels=channels,
                           callback=query_callback):
        rec = vosk.KaldiRecognizer(model, sample_rate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"], assistant_alias, assistant_cmd_list)


class SpeachToText:
    def __init__(self, model):
        self.model = vosk.Model('models_stt/' + model)
        self.sample_rate = 16000
        self.block_size = 8000
        self.device = 1
        self.d_type = 'int16'
        self.channels = 1

    def get_model(self):
        return {'model': self.model,
                'sample_rate': self.sample_rate,
                'block_size': self.block_size,
                'device': self.device,
                'd_type': self.d_type,
                'channels': self.channels}
