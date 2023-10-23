import torch
import sounddevice as sd
import time
import silero
import numpy


class VoiceModel:
    repo_or_dir = 'snakers4/silero-models_stt'
    model = 'silero_tts'

    def __init__(self, language, model_id, sample_rate, speaker, put_accent=True, put_yo=True):
        self.language = language
        self.model_id = model_id
        self.sample_rate = sample_rate
        self.speaker = speaker
        self.put_accent = put_accent
        self.put_yo = put_yo
        self.device = torch.device('cpu')
        self.audio = None
        self.model = None
        VoiceModel.create_model(self)

    def create_model(self):
        self.model, _ = torch.hub.load(repo_or_dir=VoiceModel.repo_or_dir,
                                       model=VoiceModel.model,
                                       language=self.language,
                                       speaker=self.model_id)
        self.model.to(self.device)

    def create_audio(self, text):
        self.audio = self.model.apply_tts(text=text,
                                          speaker=self.speaker,
                                          sample_rate=self.sample_rate,
                                          put_accent=self.put_accent,
                                          put_yo=self.put_yo)

    def play_audio(self, text):
        VoiceModel.create_audio(self, text)
        sd.play(self.audio, self.sample_rate)
        time.sleep(len(self.audio) / self.sample_rate)
        sd.stop()

