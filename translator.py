from translate import Translator


class TranslatorModel:
    def __init__(self, to_lang: str, from_lang: str):
        self.translator = Translator(from_lang, to_lang)

    def change_langs(self, to_lang: str, from_lang: str = None):
        if from_lang is not None:
            self.translator = Translator(from_lang, to_lang)
        else:
            self.translator = Translator(to_lang)

    def translate(self, text_to_translate: str) -> str:
        return self.translator.translate(text_to_translate)

