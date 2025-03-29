import sqlite3
import os
import json


class DatabaseInformation:

    def __init__(self):        
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        self.db_foler_path = os.path.join(base_dir, "../databases/")


    def getConnection(self, dbName):
        connection = sqlite3.connect(self.db_foler_path + dbName)
        return connection
    
    def getDatabaseInforamtion(self) -> str:
        information = ""
        with open(self.db_foler_path  + "dbDescription.json", "r", encoding="utf-8") as info:

            connectionInfo = json.load(info)
            for db, description in connectionInfo.items():
                information += f"Database {db}:\n {description}\n"
                information += "Tables in Database:\n"
                dbConnection = self.getConnection(db)
                cursor = dbConnection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    tableName = table[0]
                    information += f"Table {tableName}:\n"
                    cursor.execute(f"PRAGMA table_info({tableName});")
                    columns = cursor.fetchall()
                    information += f"{columns}\n"
        return information

if __name__ == "__main__":
    dbInfo = DatabaseInformation()
    #print(dbInfo.getDatabaseInforamtion())