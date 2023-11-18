from ttsModule import VoiceModel as textToSpeach
from translatorModule import TranslatorModel as translate
from openAIModule import TextNeuralNetwork as gpt
from sttModule import SpeachToText as speachToText, listen
from SettingsManager import SettingsManager, settings_manager
from fuzzywuzzy import fuzz

settings_manager.load_settings()

def execute_cmd(cmd: str):
    print("Виконую: "+cmd)

def recognize_cmd(cmd: str, assistant_cmd_list):
    rc = {'cmd': '', 'percent': 0}
    for word_list_key in assistant_cmd_list:
        word_list = assistant_cmd_list[word_list_key]["word_list"]
        for x in word_list:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = word_list_key
                rc['percent'] = vrt

    return rc
#
def stt_respond(voice: str, assistant_alias, assistant_cmd_list):
    #########################################
    print(voice)
    #########################################
    if voice.startswith(assistant_alias):
        cmd = recognize_cmd(filter_cmd(voice, assistant_alias), assistant_cmd_list)
        if cmd['cmd'] not in assistant_cmd_list.keys():
            print("Я вас не зрозумів")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str, assistant_alias):
    cmd = raw_voice

    for x in assistant_alias:
        cmd = cmd.replace(x, "").strip()

    return cmd



def update_settings():
    settings_manager.load_settings()
    current_settings = settings_manager.get_setting('CURRENT_SETTINGS', {})
    assistant_cmd_list = settings_manager.get_setting('ASSISTANT_CMD_LIST', {})
    assistant_alias = settings_manager.get_setting('ASSISTANT_ALIAS', {})
    assistant_stt = settings_manager.get_setting('ASSISTANT_STT', {})
    assistant_tts = settings_manager.get_setting('ASSISTANT_TTS', {})
    assistant_tra = settings_manager.get_setting('ASSISTANT_TRA', {})
    current_settings = settings_manager.get_setting('CURRENT_SETTINGS', {})
    return {
        "current_settings": current_settings,
        "assistant_cmd_list": assistant_cmd_list,
        "assistant_alias": assistant_alias,
        "assistant_stt": assistant_stt,
        "assistant_tts": assistant_tts,
        "assistant_tra": assistant_tra,
        "current_settings": current_settings
    }

def run_command_processor():
    settings = update_settings()
    current_settings = settings['current_settings']
    assistant_cmd_list = settings['assistant_cmd_list']
    assistant_alias_list = settings['assistant_alias']
    assistant_stt = settings['assistant_stt']
    assistant_tts = settings['assistant_tts']
    assistant_tra = settings['assistant_tra']
    current_settings = settings['current_settings']

    assistant_alias = tuple(assistant_alias_list)

    speachVA = speachToText(assistant_stt[current_settings['ASSISTANT_STT']]['model'])
    listen(stt_respond, speachVA.get_model(), assistant_alias, assistant_cmd_list)
