from .abstract_user import User
from modules.database.db_proxy import DBProxy

import time
import random

class AUser(User):

    def __init__(self, name: str, db: DBProxy, transaction_count: int) -> None:
        super().__init__(name, db, transaction_count)
        # Transaction query for User A
        self._query = """
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

    def run(self):
        begin_time = time.time()

        # Simulate transactions
        self.simulate()
        
        end_time = time.time()
        # Record elapsed time for reporting
        self.elapsed_time = end_time - begin_time


    def simulate(self):
        for _ in range(self._transaction_count):

            self.db.connect() # Connect to the database
            self.db.set_isolation_lvl() # Set transaction isolation level

            if random.random() < 0.5:
                self.db.update_query(self._query, ("20110101", "20111231"))

            if random.random() < 0.5:
                self.db.update_query(self._query, ("20120101", "20121231"))

            if random.random() < 0.5:
                self.db.update_query(self._query, ("20130101", "20131231"))

            if random.random() < 0.5:
                self.db.update_query(self._query, ("20140101", "20141231"))

            if random.random() < 0.5:
                self.db.update_query(self._query, ("20150101", "20151231"))

            self.db.commit() # Commit the transaction
            self.db.disconnect() # Disconnect from the database


class BUser(User):

    def __init__(self, name: str, db: DBProxy, transaction_count: int) -> None:
        super().__init__(name, db, transaction_count)
        # Transaction query for User B
        self._query = """
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

    def run(self):
        begin_time = time.time()

        # Simulate transactions
        self.simulate()
        
        end_time = time.time()
        # Record elapsed time for reporting
        self.elapsed_time = end_time - begin_time


    def simulate(self):
        for _ in range(self._transaction_count):
                
                self.db.connect()  # Connect to the database
                self.db.set_isolation_lvl()  # Set transaction isolation level

                if random.random() < 0.5:
                    self.db.select_query(self._query, ("20110101", "20111231"))

                if random.random() < 0.5:
                    self.db.select_query(self._query, ("20120101", "20121231"))

                if random.random() < 0.5:
                    self.db.select_query(self._query, ("20130101", "20131231"))

                if random.random() < 0.5:
                    self.db.select_query(self._query, ("20140101", "20141231"))

                if random.random() < 0.5:
                    self.db.select_query(self._query, ("20150101", "20151231"))

                self.db.commit() # Commit the transaction
                self.db.disconnect() # Disconnect from the database