from ttsModule import VoiceModel as vm
from translatorModule import TranslatorModel as tr
from openAIModule import TextNeuralNetwork as gpt
import json
import asyncio

#
#

text = 'Привіт, мене звати Олег. Приємно познайомитись'

with open('conf_files/languages_tts.json', 'r') as vm_config_file:
    languages = json.load(vm_config_file)

with open('conf_files/freeGPT.json', 'r') as gpt_config_file:
    gpt_configs = json.load(gpt_config_file)


#
#

async def gpt_req():
    return await freeGPT.create_prompt(trans.translate_text(text))


#
#

freeGPT = gpt(gpt_configs['model'], gpt_configs['is_quick_answer'])
vm_en = vm(languages['English']['language'], languages['English']['model_id'], languages['English']['sample_rate'],
           languages['English']['speaker'])

trans = tr('UK', 'EN')
vm_en.play_audio(trans.translate_text(text))


result = ''
if __name__ == "__main__":
    result = asyncio.run(gpt_req())

vm_en.play_audio(trans.translate_text(result))

# добавить расспознавание голоса
