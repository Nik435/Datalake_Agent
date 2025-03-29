import sqlite3
import os
import json

class DbContext:
    """
    Service class to manage user-related database operations.
    """

    def __init__(self):
        """
        Initialize the UserService with a connection to the SQLite database.

        :param db_path: Path to the SQLite database file.
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))  
        self.db_foler_path = os.path.join(base_dir, "../databases/")
        self.databaseForTable = self.buildTableDict(os.path.join(base_dir, "../databases/"))
    
    def buildTableDict(self, dbFolderPath:str)-> dict:
        databaseForTable = {}
        with open(dbFolderPath + "dbTableConnections.json", "r", encoding="utf-8") as info:

            connectionInfo = json.load(info)
            for db, tables in connectionInfo.items():
                for table in tables:
                    databaseForTable[table] = db
        return databaseForTable


    def connect(self, db_name: str):
        """
        Establish a connection to the database.
        :return: SQLite connection object.
        """
        return sqlite3.connect(self.db_foler_path + db_name)
    

    def sqlQuery(self, database:str, query:str):
        #query = "SELECT * FROM races"
        with self.connect(database) as connection:
            cursor = connection.execute(query)
            return str(cursor.fetchall())
        
    def getDbDiscription(self, db_name: str) -> str:
        with open(self.db_foler_path + "dbDescription.json", "r", encoding="utf-8") as info:
            dbInfo = json.load(info)
            description = f"Description for Database {db_name}: {dbInfo.get(db_name)}"
            return description
    
    def listTables(self, database: str) -> str:
        query = f"SELECT name FROM sqlite_master WHERE type = 'table';"
        with self.connect(database) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            tables = cursor.fetchall()
            resultTables = ""
            for table in tables:
                resultTables += f"{table[0]}, "
            return resultTables

    def getColumnNames(self, table_name):
        query = f"PRAGMA table_info('{table_name}');"
        database = self.databaseForTable[table_name]
        with self.connect(database) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            columns = str(cursor.fetchall())
            return f"Collums in requested table {table_name} from Database {database}:{columns}"
    
    def getRemainingTables(self, givenTables: list[str]) -> str:
        dataBase = self.getDbToTable(givenTables[0])
        with open(self.db_foler_path + "dbTableConnections.json", "r", encoding="utf-8") as info:
            info = json.load(info)
            tables: list[str] = info[dataBase]
            remainingTables = [x for x in tables if x not in givenTables]
            return remainingTables

    def getDbToTable(self, tableName: str) -> str:
        return self.databaseForTable[tableName]
    


if __name__ == "__main__":
    dbContext = DbContext()
    database = "american_football.sqlite"
    query = f"SELECT name FROM sqlite_master WHERE type = 'table';"
    print(dbContext.sqlQuery(database, query))