from voiceModel import VoiceModel as vm

vm_ua = vm('ua', 'v4_ua', 48000, 'mykyta')
vm_en = vm('en', 'v3_en', 48000, 'en_0')

text_ua = 'Привіт, мене звати Олег'
vm_ua.play_audio(text_ua)

text_en = 'Hello, my name is Oleg'
vm_en.play_audio(text_en)
