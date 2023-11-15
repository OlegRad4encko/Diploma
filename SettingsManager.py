import json
import default_config_assistant as default_config


class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.settings = default_config.DEFAULT__SETTINGS

    def load_settings(self):
        try:
            with open(self.filename, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = default_config.DEFAULT__SETTINGS

    def save_settings(self):
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value

    def delete_setting_from_key(self, key, key_to_remove):
        if key in self.settings and key_to_remove in self.settings[key]:
            del self.settings[key][key_to_remove]
            self.save_settings()
            self.load_settings()

    def delete_value_from_key(self, key, value):
        if key in self.settings and value in self.settings[key]:
            self.settings[key].remove(value)
            self.save_settings()
            self.load_settings()




