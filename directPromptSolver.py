from colorama import Fore
from databaseInformation import DatabaseInformation
from dbContext import DbContext
from gptApi.openAIService import OpenAIService
import tiktoken


class DirectPromptSolver:
    def __init__(self, apiService: OpenAIService):
        """
        Initializes the DirectPromptSolver with the provided apiService.
        """
        self.apiService = apiService
        self.apiModel   = apiService.getModel()
        self.promptHeader = ""
        self.dbContext = DbContext()
        self.dbInformation = DatabaseInformation()
    
    def solveTask(self, task):
        sumTokens = 0
        try:
            prompt = self.dbInformation.getDatabaseInforamtion() + f"Task to solve:{task}"
            answer = self.apiService.sendMessage(prompt)
            response = answer[0]
            sumTokens += answer[1]
            database = response.choices[0].message.parsed.args[0]
            print(Fore.BLUE +f"SQL Query: {response.choices[0].message.parsed.message}")
            result = self.dbContext.sqlQuery(database, response.choices[0].message.parsed.message)
            sqlQuery = database, response.choices[0].message.parsed.message
        except Exception as e:
            return [f"Your last message orrcued a error don't use it again: {e}", "",sumTokens]
        return [result, str(sqlQuery), sumTokens]


