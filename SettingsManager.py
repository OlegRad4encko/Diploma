import default_config_assistant as default_config
import json


class SettingsManager:
    # init
    def __init__(self, filename:str='settings.json'):
        self.filename = filename
        self.settings = default_config.DEFAULT__SETTINGS


    # loading settings
    def load_settings(self):
        try:
            with open(self.filename, 'r') as file:
                try:
                    self.settings = json.load(file)
                except json.JSONDecodeError:
                    self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = default_config.DEFAULT__SETTINGS


    # saving settings
    def save_settings(self):
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)


    # getting settings
    def get_setting(self, key:str, default=None):
        return self.settings.get(key, default)


    # setting settings
    def set_setting(self, key:str, value):
        self.settings[key] = value


    # deleting settings from key
    def delete_setting_from_key(self, key:str, key_to_remove:str):
        if key in self.settings and key_to_remove in self.settings[key]:
            del self.settings[key][key_to_remove]
            self.save_settings()
            self.load_settings()


    # deleting value by key
    def delete_value_from_key(self, key:str, value:str):
        if key in self.settings and value in self.settings[key]:
            self.settings[key].remove(value)
            self.save_settings()
            self.load_settings()


# creating settings_manager object
settings_manager = SettingsManager()



