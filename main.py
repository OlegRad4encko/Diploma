from ttsModule import VoiceModel as vm
from translatorModule import TranslatorModel as tr
from openAIModule import TextNeuralNetwork as gpt
from sttModule import SpeachToText as stt
from SettingsManager import SettingsManager
from sttModule import listen
from fuzzywuzzy import fuzz
import sys
import json
import asyncio
import os
from server import *
from trayMenu import *
from multiprocessing import Process



if __name__ == '__main__':
    tray_process = Process(target=startTray)
    tray_process.start()
    tray_process.join()


#    run_server()





# def execute_cmd(cmd: str):
#     print("Виконую: "+cmd)
#
# def recognize_cmd(cmd: str):
#     rc = {'cmd': '', 'percent': 0}
#     for c, v in config.ASSISTANT_CMD_LIST.items():
#         for x in v:
#             vrt = fuzz.ratio(cmd, x)
#             if vrt > rc['percent']:
#                rc['cmd'] = c
#                rc['percent'] = vrt
# #
#     return rc
# #
# def stt_respond(voice: str):
#     print(voice)
#     if voice.startswith(config.ASSISTANT_ALIAS):
#         cmd = recognize_cmd(filter_cmd(voice))
#
#         if cmd['cmd'] not in config.ASSISTANT_CMD_LIST.keys():
#             print("Я вас не зрозумів")
#         else:
#             execute_cmd(cmd['cmd'])
#
#
# def filter_cmd(raw_voice: str):
#     cmd = raw_voice
#
#     for x in config.ASSISTANT_ALIAS:
#         cmd = cmd.replace(x, "").strip()
#
#     return cmd
#
# stt = stt('vosk-model-uk-v3')
# listen(stt_respond, stt.get_model())



# async def gpt_req(text_to_gpt):
#     freeGPT = gpt()
#     return await freeGPT.create_prompt(text_to_gpt)
#
# if __name__ == "__main__":
#     print(asyncio.run(gpt_req("Что такое Дота?")))