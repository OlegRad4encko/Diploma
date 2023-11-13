from ttsModule import VoiceModel as vm
from translatorModule import TranslatorModel as tr
from openAIModule import TextNeuralNetwork as gpt
from sttModule import SpeachToText as stt
from sttModule import listen
from fuzzywuzzy import fuzz
import sys
import json
import asyncio
import config_assistant as config


from flask import Flask, send_file, render_template, url_for
import webbrowser

app = Flask(__name__, template_folder='web')

@app.route('/')
def serve_html():
    return render_template('index.html')

@app.route('/other_settings')
def other_settings():
    return render_template('otherSettings.html')

@app.route('/src/styles.css')
def serve_css():
    return send_file('src/styles.css', mimetype='text/css')



def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    import threading
    server_thread = threading.Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000})
    server_thread.start()
    open_browser()
    server_thread.join()






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