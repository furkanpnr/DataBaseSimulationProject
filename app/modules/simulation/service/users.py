import datetime
import traceback
from modules.database.db_proxy import DBProxy
import datetime

class AUser:
    def __init__(self,db: DBProxy):
        self.db = db
        
    def update(self):
        try:
            self.db.execute_update_query("""UPDATE [AdventureWorks2019].[Production].[Product]
                                            SET [SafetyStockLevel] = [SafetyStockLevel] - 1
                                            WHERE [ProductId] = 752""")
            print("Update successful")
        except Exception as e:
            print("Error occurred while updating the database:")
            print(traceback.format_exc())  # Print detailed traceback
            # You can log the error to a file or log management system here
    
    def start(self):
        self.update()


class BUser:
    def __init__(self,db: DBProxy):
        self.db = db

    def read_data(self):
        try:
            result = self.db.execute_select_query("""SELECT [SafetyStockLevel], [ProductNumber]
                                                     FROM [AdventureWorks2019].[Production].[Product]
                                                     WHERE [ProductId] = 752""")
            print("Data read successfully:", result)
        except Exception as e:
            print("Error occurred while reading data from the database:")
            print(traceback.format_exc())  # Print detailed traceback
            # You can log the error to a file or log management system here

    def start(self):
        self.read_data()

        