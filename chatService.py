from datalakeAgent import DatalakeAgent
from colorama import Fore

class ChatService:
    def __init__(self, chatAgent: DatalakeAgent):
        """
        Initializes the ChatService with the provided apiService.
        """
        self.chatAgent = chatAgent
        self.apiModel = chatAgent.getModel()


    def startChat(self):
        """
        Start the chat with the OpenAI model, taking input from the user and displaying responses.
        """

        print(f"Chatbot {self.apiModel} is ready! Type 'exit' to end the chat.")
        
        # communication loop
        while True:
            user_message = input("\nYou: ")  
            if user_message.lower() == "exit":
                print("Exiting chat. Goodbye!")
                break 
    
            response = self.chatAgent.solveTask(user_message)
            
            print(Fore.YELLOW + f"Model {self.apiModel}: {response}")