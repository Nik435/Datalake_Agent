import os
from directPromptSolver import DirectPromptSolver
from evaluation import Evaluation
from gptApi.setupApi import SetupApi
from chatService import ChatService
from datalakeAgent import DatalakeAgent


def main():
    """
    Main function to demonstrate the usage of the OpenAI API communicator.
    """
    try:
        main_dir = os.path.dirname(__file__)  # Verzeichnis von main.py
        openAiSettings = os.path.join(os.path.dirname(main_dir), "openAiSettings.json")
        promptSettings = os.path.join(os.path.dirname(__file__), "gptApi/promptSettings.json")

        # Initialize SetupApi with the configuration file
        setup_api = SetupApi(openAiSettings, promptSettings)
        
        # Create an OpenAIService instance with direct prompt
        apiServiceDP = setup_api.setService("system_prompt_dp")

        #Create an OpenAIService instance with chat agent
        apiServiceChatAgent = setup_api.setService("system_prompt_ca")

        #Create ChatAgent
        datalakeAgent = DatalakeAgent(apiServiceChatAgent)

        #directSolver = DirectPromptSolver(apiServiceDP)

        # Create ChatService
        chatService = ChatService(datalakeAgent)

        chatService.startChat()

        #Create Evaluation
        #evaluation = Evaluation(datalakeAgent, directSolver)
        
        #evaluation.start()
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()