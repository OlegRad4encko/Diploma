from freeGPT import AsyncClient
from SettingsManager import SettingsManager, settings_manager
import asyncio



class TextNeuralNetwork:
    def __init__(self):
        settings_manager.load_settings()
        current_settings = settings_manager.get_setting('CURRENT_SETTINGS', {})

        self.model = "gpt3"
        self.is_quick_answer = current_settings['IS_QUICK_ANSWER']


    # chatGPT request
    async def create_prompt(self, prompt):
        try:
            if self.is_quick_answer == 'True':
                prompt += ' (Дай найкоротшу відповідь на тій мові, яка було до дужок)'
                resp = await AsyncClient.create_completion(self.model, prompt)
                return resp
            else:
                resp = await AsyncClient.create_completion(self.model, prompt)
                return resp

        except Exception as e:
            return f"Error {e}"



