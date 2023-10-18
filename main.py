from voiceModel import VoiceModel as vm
from translator import TranslatorModel as tr

languages = {
    'Ukraine': {
        'language': 'ua',
        'model_id': 'v4_ua',
        'sample_rate': 48000,
        'speaker': 'mykyta'
    },
    'English': {
        'language': 'en',
        'model_id': 'v3_en',
        'sample_rate': 48000,
        'speaker': 'en_0'
    },
    'German': {
        'language': 'de',
        'model_id': 'v3_de',
        'sample_rate': 48000,
        'speaker': 'karlsson'
    }
}
vm_en = vm(languages['English']['language'], languages['English']['model_id'], languages['English']['sample_rate'],
           languages['English']['speaker'])
translate = tr('UK', 'EN')
vm_en.play_audio(translate.translate('Добрий ранок'))

# vm_ua = vm(languages['Ukraine']['language'], languages['Ukraine']['model_id'], languages['Ukraine']['sample_rate'],
#           languages['Ukraine']['speaker'])



