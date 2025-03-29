from gptApi.openAIService import OpenAIService
from dbContext import DbContext
from colorama import Fore

class DatalakeAgent:
    def __init__(self, apiService: OpenAIService):
        """
        Initializes the Datalake Agent with the provided apiService.
        """
        self.apiService = apiService
        self.apiModel   = apiService.getModel()
        self.promptHeader = ""
        self.dbContext = DbContext()

    def solveTask(self, task:str):
        """
        Start the solving process with the model.
        """
        print(f"The task will be solved...")

        counter = 0
        sumTokens = 0
        requestedArgs = []
        result = ""
        sqlQuery = ""
        inSolvingProcess = True
        response = ""
        currentInfo = ""
        prompt = self.promptHeader + "Task to solve: " + task + "\n"
        # communication loop
        while inSolvingProcess:
            counter += 1
            try:
                if counter > 10:
                    print("Generate and send the SQL query immediately for the task. No further questions or clarifications are needed.")
                    answer = self.apiService.sendMessage("Generate and send the SQL query immediately for the task. No further questions or clarifications are needed.\n" + "Task: " + task)
                    response = answer[0]
                    sumTokens += answer[1]
                    print(f"SQL Query: {response.choices[0].message.parsed.message}")
                    database = response.choices[0].message.parsed.args[0]
                    result = self.dbContext.sqlQuery(database, response.choices[0].message.parsed.message)
                    break
                print(Fore.GREEN + "Agent: \n" + prompt + currentInfo)
                answer = self.apiService.sendMessage(prompt + currentInfo)
                response = answer[0]
                sumTokens += answer[1]
                print(Fore.BLUE + "API Respones: \n" + str(response.choices[0].message.parsed))
                #previousRequest = response.choices[0].message.parsed           
                currentInfo = ""
                match response.choices[0].message.parsed.keyword:
                    case "GetDBDescription":
                        for db in response.choices[0].message.parsed.args:
                            #if set in requestedArgs:
                                #currentInfo += f"You have already requested information about {set}. Use another request\n"
                            requestedArgs.append(set)
                            currentInfo += f"{self.dbContext.getDbDiscription(db)} \n"
                    case "GetTables":
                        for db in response.choices[0].message.parsed.args:
                            #if set in requestedArgs:
                                #currentInfo += f"You have already requested information about {set}. Use another request\n"
                            requestedArgs.append(set)
                            currentInfo += f"Tables in requested dataset {set}: {self.dbContext.listTables(db)} \n"
                    case "GetColumns":
                        for table in response.choices[0].message.parsed.args:
                            #if table in requestedArgs:
                                #currentInfo += f"You have already requested information about {table}. Use another request\n"
                            requestedArgs.append(table)
                            currentInfo += f"{self.dbContext.getColumnNames(table)} \n"
                        currentInfo += f"Other tables in this dataset: {self.dbContext.getRemainingTables(response.choices[0].message.parsed.args)}"
                    case "DbQueryFinalSQL":
                        print(f"SQL Query: {response.choices[0].message.parsed.message}")
                        database = response.choices[0].message.parsed.args[0]
                        result= self.dbContext.sqlQuery(database, response.choices[0].message.parsed.message) 
                        sqlQuery = response.choices[0].message.parsed.message            
                        inSolvingProcess = False
                    case _:
                        inSolvingProcess = False
            except Exception as e:
                inSolvingProcess = False
                result = f"Your last message orrcued a error don't use it again: {e}"  
        return [result, str(sqlQuery), sumTokens]
    
    def getModel(self) -> str:
        return self.apiModel