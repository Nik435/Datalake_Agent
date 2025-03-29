import openai
from openai import OpenAI
from pydantic import BaseModel
import tiktoken

class OpenAIService:
    def __init__(self, apiKey: str, model: str, systemPrompt: str):
        """
        Initializes the communicator with an API key and a model name.

        :param api_key: Your OpenAI API key
        :param model: The name of the OpenAI model to use
        """
        self.apiKey = apiKey
        self.model = model
        self.systemPrompt = systemPrompt
        self.client = OpenAI(api_key=apiKey)

    def sendMessage(self, message: str):
        """
        Sends a message to the OpenAI API and returns the response.

        :param message: The user input message
        :param system_prompt: An optional system context for the model
        :param temperature: Creativity level for the response (between 0 and 1)
        :param max_tokens: Maximum length of the response
        :return: The model's response
        """
        messages = []
        if message.startswith("Generate and send the SQL"):
            messages.append({"role": "system", "content": "The final SQL query must be delivered in the following format:\nkeywords: 'DbQueryFinalSQL'\nargs: Specify the databases the query will be executed on.\nmessage: Contain the SQL query itself."})
        else:
            messages.append({"role": "system", "content": self.systemPrompt})
        messages.append({"role": "user", "content": message})
        enc = tiktoken.encoding_for_model(self.model)
        tokens = enc.encode(str(messages))

        print(f"Amount of tokens for: {len(tokens)}")
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=Resopnseformat,
                temperature=0.1
            )
            return response , len(tokens)
        except Exception as e:
            return f"An error occurred: {e}", 0
    
    '''
    Returns Model-Type that is currently used
    '''
    def getModel(self) -> str:
        return self.model

class Resopnseformat(BaseModel):
    keyword: str
    args: list[str]
    message: str
