from freeGPT import AsyncClient
import asyncio


class TextNeuralNetwork:
    def __init__(self, model: str = "gpt3"):
        self.model = model
        self.isQuickAnswer = True  # need make configurable

    async def create_prompt(self, prompt):
        try:
            resp = await AsyncClient.create_completion(self.model, prompt)
            return resp
        except Exception as e:
            return f"Error {e}"



