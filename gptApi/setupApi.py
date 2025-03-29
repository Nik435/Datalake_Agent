import json
from gptApi.openAIService import OpenAIService

class SetupApi:
    def __init__(self, apiSettings: str, promptSettings: str):
        """
        Handles the setup of the API by reading configuration from a JSON file.

        :param config_file: Path to the JSON configuration file
        """
        self.apiSettings = apiSettings
        self.promptSettings = promptSettings
        self.config = self.loadConfig()
        self.promptConfig = self.loadPromptConfig()

    def loadConfig(self) -> dict:
        """
        Loads the configuration from the JSON file.

        :return: Dictionary containing API settings
        """
        try:
            with open(self.apiSettings, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.apiSettings}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in configuration file '{self.apiSettings}'.")
    
    def loadPromptConfig(self) -> dict:
        """
        Loads the prompt configuration from the JSON file.

        :return: Dictionary containing prompt settings
        """
        try:
            with open(self.promptSettings, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.promptSettings}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in configuration file '{self.promptSettings}'.")

    def setService(self, systemPromptName:str) -> OpenAIService:
        """
        Creates and returns an OpenAICommunicator instance based on the configuration.

        :return: An initialized OpenAICommunicator instance
        """
        apiKey = self.config.get("api_key", "")
        model = self.config.get("model", "gpt-4o-mini")
        systemPrompt = self.promptConfig.get(systemPromptName, "You are a helpful assistant.")
        if not apiKey:
            raise ValueError("API key is missing in the configuration.")
        return OpenAIService(apiKey=apiKey, model=model, systemPrompt=systemPrompt)


