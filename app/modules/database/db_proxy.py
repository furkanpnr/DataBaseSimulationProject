import pyodbc
from config import DATABASE, SERVER

connectionString =  f"DRIVER={{SQL Server}}; SERVER={SERVER}; DATABASE={DATABASE}; Trusted_Connection=yes;"


class DBProxy:
    def __init__(self) -> None:
        self.conn = pyodbc.connect(connectionString)
        self.cursor = self.connection.cursor()

    def _connect(self) -> None:
        try:
            self.conn = pyodbc.connect(connectionString)
            print("Connected to the database")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
    
    def _disconnect(self) -> None:
        try:
            if self.conn:
                self.conn.close()
                print("Disconnected from the database")
        except Exception as e:
            print(f"Error disconnecting from the database: {e}")
        

    def __del__(self):
        self._disconnect()

    

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
    

    def update_sales_order_detail(self, begin_date, end_date):
        """ Update Query for User A

            args: begin_date , end_date > yyyy-mm-dd
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
        
    
    def select_sales_order_detail(self, begin_date, end_date):
        """ Select Query for User B

            args: begin_date , end_date > yyyy-mm-dd
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