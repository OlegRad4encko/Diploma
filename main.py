from ttsModule import VoiceModel as vm
from translatorModule import TranslatorModel as tr
from openAIModule import TextNeuralNetwork as gpt
import json
import asyncio

with open('conf_files/languages_tts.json', 'r') as vm_config_file:
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

trans.change_langs('EN')


async def gpt_req():
    text_nn = gpt()
    result = await text_nn.create_prompt(trans.translate_text(text))
    print(result)


if __name__ == "__main__":
    asyncio.run(gpt_req())

# добавить расспознавание голоса
