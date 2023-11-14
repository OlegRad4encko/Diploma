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
import config_assistant as config
from flask import Flask, send_file, render_template, url_for, request
import webbrowser



# configs of VA assistant
settings_manager = SettingsManager()
settings_manager.load_settings()
assistant_stt = settings_manager.get_setting('ASSISTANT_STT', {})
assistant_tts = settings_manager.get_setting('ASSISTANT_TTS', {})
assistant_tra = settings_manager.get_setting('ASSISTANT_TRA', {})
current_settings = settings_manager.get_setting('CURRENT_SETTINGS', {})


# config for local web server =======
web_config = ''
with open('web_config.json', 'r') as file:
    web_config = json.load(file)

# web Server ========================
app = Flask(__name__, template_folder='web')

@app.route('/', methods=['GET', 'POST'])
def serve_html():
    if request.method == 'POST':
        current_settings['ASSISTANT_TTS'] = request.form.get('ttsLang')
        current_settings['ASSISTANT_STT'] = request.form.get('sttLang')
        current_settings['ASSISTANT_TRA'] = request.form.get('transLang')

        settings_manager.set_setting('CURRENT_SETTINGS', current_settings)
        settings_manager.save_settings()

    return render_template('index.html', assistant_stt=assistant_stt,
        assistant_tts=assistant_tts,
        assistant_tra=assistant_tra,
        current_settings=current_settings)

@app.route('/other_settings', methods=['GET', 'POST'])
def other_settings():
    if request.method == 'POST':
        if request.form.get('SpeakTheAnswer') == None:
            current_settings['SPEAK_THE_ANSWER'] = False
        else:
            current_settings['SPEAK_THE_ANSWER'] = True
        if request.form.get('IsQuickAnswer') == None:
            current_settings['IS_QUICK_ANSWER'] = False
        else:
            current_settings['IS_QUICK_ANSWER'] = True

        settings_manager.set_setting('CURRENT_SETTINGS', current_settings)
        settings_manager.save_settings()

    return render_template('otherSettings.html', current_settings=current_settings)

@app.route('/add_languages')
def add_languages():
    return render_template('addLanguages.html')



@app.route('/src/styles.css')
def serve_css():
    return send_file('src/styles.css', mimetype='text/css')

def open_browser():
    webbrowser.open('http://'+str(web_config['host'])+':'+str(web_config['port'])+'/')

if __name__ == '__main__':
    import threading
    server_thread = threading.Thread(target=app.run, kwargs={'host': web_config['host'], 'port': web_config['port']})
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