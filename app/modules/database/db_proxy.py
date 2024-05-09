import pyodbc
from .enums import IsolationLevel

class DBProxy:
    
    def __init__(self, 
                 server_name: str, 
                 database_name: str,
                 isolation_level: IsolationLevel) -> None:
        
        self.server_name = server_name
        self.database_name = database_name
        self.isolation_level = isolation_level
        
        self.connectionString = f"DRIVER={{SQL Server}}; SERVER={server_name}; DATABASE={database_name}; Trusted_Connection=yes;"
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        try:
            self.conn = pyodbc.connect(self.connectionString)
            self.cursor = self.conn.cursor()
            print("Connected to the database")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
    
    def disconnect(self) -> None:
        try:
            if self.conn:
                self.conn.close()
                print("Disconnected from the database")
        except Exception as e:
            print(f"Error disconnecting from the database: {e}")

    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.disconnect()

    def execute_select_query(self, query: str) -> list:
        """Select query executor

        Args:
            query (str): SQL query to execute
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing select query: {e}")
            return []
        
    def execute_update_query(self, query: str) -> bool:
        """Update query executor

        Args:
            query (str): SQL query to execute
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error executing update query: {e}")
            return False
    
    def update_sales_order_detail(self, begin_date: str, end_date: str):
        """ Update Query for User A
        
        Args:
            begin_date (str): yyyy-mm-dd
            end_date (str): yyyy-mm-dd
        """

        query = """
            UPDATE Sales.SalesOrderDetail
            SET UnitPrice = UnitPrice * 10.0 / 10.0
            WHERE UnitPrice > 100
            AND EXISTS (
                SELECT *
                FROM Sales.SalesOrderHeader
                WHERE Sales.SalesOrderHeader.SalesOrderID = Sales.SalesOrderDetail.SalesOrderID
                AND Sales.SalesOrderHeader.OrderDate BETWEEN ? AND ?
                AND Sales.SalesOrderHeader.OnlineOrderFlag = 1
            )
        """

        try: 
            self.cursor.execute(query, begin_date, end_date)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating SalesOrderDetail: {e}")
            return False
        
    def select_sales_order_detail(self, begin_date: str, end_date: str):
        """ Select Query for User B
        
        Args:
            begin_date (str): yyyy-mm-dd
            end_date (str): yyyy-mm-dd
        """
        
        query = """
            SELECT SUM(Sales.SalesOrderDetail.OrderQty)
            FROM Sales.SalesOrderDetail
            WHERE UnitPrice > 100
            AND EXISTS (
                SELECT *
                FROM Sales.SalesOrderHeader
                WHERE Sales.SalesOrderHeader.SalesOrderID = Sales.SalesOrderDetail.SalesOrderID
                AND Sales.SalesOrderHeader.OrderDate BETWEEN ? AND ?
                AND Sales.SalesOrderHeader.OnlineOrderFlag = 1
            )
        """

        try:
            self.cursor.execute(query, begin_date, end_date)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error selecting SalesOrderDetail: {e}")
            return None
    
    def set_transaction_isolation_level(self):
        """Sets transaction isolation level"""
        level = self.isolation_level

        isolation_level_query = f"SET TRANSACTION ISOLATION LEVEL {level.value}"
        
        try:
            self.conn.execute(isolation_level_query)
            print(f"Isolation level set to {level.name}")
        except Exception as e:
            print(f"Error setting isolation level: {e}")
