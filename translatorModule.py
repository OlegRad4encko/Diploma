from translate import Translator


class TranslatorModel:
    # init
    def __init__(self, from_lang: str, to_lang: str):
        self.to_lang = to_lang
        self.from_lang = from_lang


    # changing the language
    def change_langs(self, to_lang: str, from_lang: str = None) -> None:
        self.to_lang = to_lang
        if from_lang is not None:
            self.from_lang = from_lang


    # translating function
    def translate_text(self, text_to_translate: str) -> str:
        translator = Translator(from_lang=self.from_lang, to_lang=self.to_lang)
        return translator.translate(text_to_translate)

    # to_lang getter
    def get_to_lang(self):
        pass


    # to_lang setter
    def set_to_lang(self):
        pass


    # from_lang getter
    def get_from_lang(self):
        pass


    # from_lang setter
    def set_from_lang(self):
        pass