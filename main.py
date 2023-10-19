from voiceModel import VoiceModel as vm
from translator import TranslatorModel as tr
import json

with open('languages.json', 'r') as vm_config_file:
    languages = json.load(vm_config_file)


vm_de = vm(languages['German']['language'], languages['German']['model_id'], languages['German']['sample_rate'],
           languages['German']['speaker'])
vm_en = vm(languages['English']['language'], languages['English']['model_id'], languages['English']['sample_rate'],
           languages['English']['speaker'])

text = 'Привіт, мене звати Олег. Приємно познайомитись'

trans = tr('UK', 'EN')
vm_en.play_audio(trans.translate_text(text))

trans.change_langs('DE')
vm_de.play_audio(trans.translate_text(text))




