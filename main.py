from ttsModule import VoiceModel as vm
from translatorModule import TranslatorModel as tr
from openAIModule import TextNeuralNetwork as gpt
from sttModule import SpeachToText as stt
from SettingsManager import SettingsManager
import sys
import json
import asyncio
import os
from trayMenu import TrayMenu, startTray
from multiprocessing import Process
from fuzzywuzzy import fuzz
from sttModule import SpeachToText as stt, listen



if __name__ == '__main__':
    tray_process = Process(target=startTray)
    tray_process.start()



# async def gpt_req(text_to_gpt):
#     freeGPT = gpt()
#     return await freeGPT.create_prompt(text_to_gpt)
#
# if __name__ == "__main__":
#     print(asyncio.run(gpt_req("Что такое Дота?")))