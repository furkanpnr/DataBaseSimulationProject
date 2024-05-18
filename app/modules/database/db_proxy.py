import pyodbc
from .enums import IsolationLevel
from threading import current_thread

from rich import print


class DBProxy:
    
    def __init__(self, 
                 server_name: str, 
                 database_name: str,
                 isolation_level: IsolationLevel) -> None:
        
        self.server_name = server_name
        self.database_name = database_name
        self.isolation_level = isolation_level
        
        self.connectionString = f"DRIVER={{SQL Server}}; SERVER={self.server_name}; DATABASE={self.database_name}; Trusted_Connection=yes;"
        self.conn = None
        self.cursor = None

        self._encountered_deadlock_num = 0

   
    def connect(self) -> None:
        """Connects to the database using the connection string
           İf connection is successful, creates a cursor object
        """
        try:
            self.conn = pyodbc.connect(self.connectionString)
        except pyodbc.Error as e:
            print(f"[bold red]{current_thread().name} Had an error connecting to DB, Code: {e.args[0]}, Message: {e.args[1]} \n")
        except Exception as e:
            print(f"[bold red]{current_thread().name} Had an error connecting to DB: {e} \n")
        else:
            if self.conn:
                print(f"[bold green]{current_thread().name} connected to DB \n")
                self.cursor = self.conn.cursor()


    def disconnect(self) -> None:
        """Disconnects from the database
           Sets the connection and cursor objects to None after closing the connection
        """
        try:
            if self.conn:
                self.conn.close()
        except pyodbc.Error as e:
            print(f"[bold red]{current_thread().name} Had an error disconnecting from DB, Code: {e.args[0]}, Message: {e.args[1]} \n")
        except Exception as e:
            print(f"[bold red]{current_thread().name} Had an error disconnecting from DB: {e} \n")
        else:
            print(f"[bold bright_black]{current_thread().name} disconnected from DB \n")
            self.conn = None
            self.cursor = None

    
    def commit(self) -> None:
        """Commits the transaction to the database
        """
        try:
            self.conn.commit()
        except pyodbc.Error as e:
            print(f"[bold red]{current_thread().name} Had an error committing to DB, Code: {e.args[0]}, Message: {e.args[1]} \n")
        except Exception as e:
            print(f"[bold red]{current_thread().name} Had an error committing to DB: {e} \n")
        else:
            print(f"[bold bright_cyan]{current_thread().name} committed to DB \n")
    
    
    def set_isolation_lvl(self) -> None:
        """Sets the isolation level for the transaction
        """
        level = self.isolation_level.value
        try:
            self.cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")
        except pyodbc.Error as e:
            print(f"[bold red]{current_thread().name} Had an error setting isolation level to {level}, Code: {e.args[0]}, Message: {e.args[1]} \n")
        except Exception as e:
            print(f"[bold red]{current_thread().name} Had an error setting isolation level to {level}: {e} \n")
        else:
            print(f"[bold yellow]{current_thread().name} set isolation level to {level} \n")


    def update_query(self, query: str, params: tuple) -> None:
        """Executes an update query on the database

        Args:
            query (str): Update query to execute on the database
            params (tuple): Parameters for the query
        """
        try:
            self.cursor.execute(query, params)
        except pyodbc.Error as e:
            print(f"{current_thread().name} Had an error executing a query on db, Code: {e.args[0]}, Message: {e.args[1]}")
            # If deadlock occurs, increment the counter
            if e.args[0] == 40001 or "deadlock" in e.args[1].lower():
                self._encountered_deadlock_num += 1

        except Exception as e:
            print(f"{current_thread().name} Had an error executing a query on db: {e}")
        else:
            print(f"{current_thread().name} executed a query on db with the parameters {params}")


    def select_query(self, query: str, params: tuple) -> list:
        """Executes a select query on the database

        Args:
            query (str): Select query to execute on the database
            params (tuple): Parameters for the query

        Returns:
            list: Result of the query
        """
        try:
            self.cursor.execute(query, params)
        except pyodbc.Error as e:
            print(f"{current_thread().name} Had an error executing a query on db, Code: {e.args[0]}, Message: {e.args[1]}")
            # If deadlock occurs, increment the counter
            if e.args[0] == 40001 or "deadlock" in e.args[1].lower():
                self._encountered_deadlock_num += 1

        except Exception as e:
            print(f"{current_thread().name} Had an error executing a query on db: {e}")
        else:
            result = self.cursor.fetchall()
            print(f"{current_thread().name} executed a query on db and the result is: {result}")
            return result


    # def update_sales_order_detail(self, begin_date: str, end_date: str):
    #     """ Update Query for User A
        
    #     Args:
    #         begin_date (str): yyyy-mm-dd
    #         end_date (str): yyyy-mm-dd
    #     """

    #     query = """
    #         UPDATE Sales.SalesOrderDetail
    #         SET UnitPrice = UnitPrice * 10.0 / 10.0
    #         WHERE UnitPrice > 100
    #         AND EXISTS (
    #             SELECT *
    #             FROM Sales.SalesOrderHeader
    #             WHERE Sales.SalesOrderHeader.SalesOrderID = Sales.SalesOrderDetail.SalesOrderID
    #             AND Sales.SalesOrderHeader.OrderDate BETWEEN ? AND ?
    #             AND Sales.SalesOrderHeader.OnlineOrderFlag = 1
    #         )
    #     """

    #     self.cursor.execute(query, begin_date, end_date)
     
        
    # def select_sales_order_detail(self, begin_date: str, end_date: str):
    #     """ Select Query for User B
        
    #     Args:
    #         begin_date (str): yyyy-mm-dd
    #         end_date (str): yyyy-mm-dd
    #     """
        
    #     query = """
    #         SELECT SUM(Sales.SalesOrderDetail.OrderQty)
    #         FROM Sales.SalesOrderDetail
    #         WHERE UnitPrice > 100
    #         AND EXISTS (
    #             SELECT *
    #             FROM Sales.SalesOrderHeader
    #             WHERE Sales.SalesOrderHeader.SalesOrderID = Sales.SalesOrderDetail.SalesOrderID
    #             AND Sales.SalesOrderHeader.OrderDate BETWEEN ? AND ?
    #             AND Sales.SalesOrderHeader.OnlineOrderFlag = 1
    #         )
    #     """

    #     self.cursor.execute(query, begin_date, end_date)
    #     return self.cursor.fetchall()