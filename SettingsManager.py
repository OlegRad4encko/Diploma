import json

class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.settings = {}

    def load_settings(self):
        try:
            with open(self.filename, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {}

        print(self.settings)

    def save_settings(self):
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value

