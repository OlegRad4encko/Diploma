from translate import Translator


class TranslatorModel:
    def __init__(self, from_lang: str, to_lang: str):
        self.to_lang = to_lang
        self.from_lang = from_lang

    def change_langs(self, to_lang: str, from_lang: str = None):
        self.to_lang = to_lang
        if from_lang is not None:
            self.from_lang = from_lang

    def translate_text(self, text_to_translate: str) -> str:
        translator = Translator(from_lang=self.from_lang, to_lang=self.to_lang)
        return translator.translate(text_to_translate)


    # разобраться с изменением языка
