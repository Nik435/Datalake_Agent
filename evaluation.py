from directPromptSolver import DirectPromptSolver
from datalakeAgent import DatalakeAgent
from colorama import Fore
import pandas as pd
import os
from tqdm import tqdm

class Evaluation:
    def __init__(self, chatAgent: DatalakeAgent, directSolver: DirectPromptSolver):
        """
        Initializes the ChatService with the provided apiService.
        """
        self.chatAgent = chatAgent
        self.directSolver = directSolver
        self.apiModel = chatAgent.getModel()
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        self.evaluation_foler_path = os.path.join(base_dir, "evaluations/")


    def start(self):
        """
        Start the chat with the OpenAI model and evaluate on the tasks
        """
        print(self.evaluation_foler_path)

        df = pd.read_csv(self.evaluation_foler_path + 'tasks.csv')
        print(df.columns)
        answersCA = []
        answersDP = []
        tasks = df['Task']

        print(tasks)

        print(f"Chatbot {self.apiModel} is ready! Type 'exit' to end the chat.")
        for i in tqdm(range(len(tasks))):
            task = tasks[i]
            resultDS = self.directSolver.solveTask(task)
            print(Fore.MAGENTA +f"Result with direct Prompt{resultDS}")
            if (len(resultDS[0]) > 2000):
                resultDS[0] = "To long answer"
            answersDP.append(resultDS)

            resultCA = self.chatAgent.solveTask(task)
            print(Fore.YELLOW +f"Result with Agent:{resultCA}")
            if (len(resultCA[0]) > 2000):
                resultCA[0] = "To long answer"
            answersCA.append(resultCA)
        

        df['Answer'] = [item[0] for item in answersDP]
        df['Used SQL command'] = [item[1] for item in answersDP]
        df['Amount of Tokens'] = [item[2] for item in answersDP]

        df.to_csv(self.evaluation_foler_path + 'answersDP.csv', index=False)

        df['Answer'] = [item[0] for item in answersCA]
        df['Used SQL command'] = [item[1] for item in answersCA]
        df['Amount of Tokens'] = [item[2] for item in answersCA]
        df.to_csv(self.evaluation_foler_path + 'answersCA.csv', index=False)


        