from notificationModule import show_notification
import json
import torch
import sounddevice as sd
import time
import silero
import numpy
import wave
import sys
import os

class VoiceModel:
    repo_or_dir = 'snakers4/silero-models'
    model = 'silero_tts'

    # init
    def __init__(self, language:str, model_id:str, sample_rate:str, speaker:str, put_accent:bool =True, put_yo:bool =True):
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


    # create model method
    def create_model(self):
        sys.stderr = open(os.devnull, "w")
        self.model, _ = torch.hub.load(repo_or_dir=VoiceModel.repo_or_dir,
                                       model=VoiceModel.model,
                                       language=self.language,
                                       speaker=self.model_id)
        self.model.to(self.device)


    # create audio method
    def create_audio(self, text:str):
        try:
            self.audio = self.model.apply_tts(text=text,
                                          speaker=self.speaker,
                                          sample_rate=self.sample_rate,
                                          put_accent=self.put_accent,
                                          put_yo=self.put_yo)
        except ValueError:
            show_notification("Голосовий помічник","Я вас не зрозумів")


    # play audio method
    def play_audio(self, text:str):
        try:
            VoiceModel.create_audio(self, text)
            sd.play(self.audio, self.sample_rate)
            time.sleep(len(self.audio) / self.sample_rate)
            sd.stop()
        except TypeError:
            show_notification("Голосовий помічник","Я вас не зрозумів")



