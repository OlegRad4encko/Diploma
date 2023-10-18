from voiceModel import VoiceModel as vm
from translator import TranslatorModel as tr
import json

with open('languages.json', 'r') as vm_config_file:
    languages = json.load(vm_config_file)

vm_en = vm(languages['English']['language'], languages['English']['model_id'], languages['English']['sample_rate'],
           languages['English']['speaker'])
translate = tr('UK', 'EN')
vm_en.play_audio(translate.translate('Добрий ранок'))

# vm_ua = vm(languages['Ukraine']['language'], languages['Ukraine']['model_id'], languages['Ukraine']['sample_rate'],
#           languages['Ukraine']['speaker'])



