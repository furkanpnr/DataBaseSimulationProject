from .abstract_user import User
from modules.database.db_proxy import DBProxy

from datetime import datetime
import random


class AUser(User):

    def __init__(self, db: DBProxy):
        super().__init__(db)

    def start(self):
        beginTime = datetime.now()
        
        self.simulate()

        endTime = datetime.now()
        elapsed = endTime - beginTime
        print("Elapsed Time:", elapsed)  # Record elapsed time for reporting

    def simulate(self):
        for _ in range(100):

            # Connect to the DB
            self.db.connect()
            self.db.set_transaction_isolation_level()

            if random.random() < 0.5:
                self._update("20110101", "20111231")

            if random.random() < 0.5:
                self._update("20120101", "20121231")

            if random.random() < 0.5:
                self._update("20130101", "20131231")

            if random.random() < 0.5:
                self._update("20140101", "20141231")

            if random.random() < 0.5:
                self._update("20150101", "20151231")

    def _update(self, begin_date, end_date):
        self.db.update_sales_order_detail(begin_date, end_date)

class BUser(User):
    def __init__(self, db: DBProxy):
        super().__init__(db)

    def start(self):
        beginTime = datetime.now()
        
        self.simulate()

        endTime = datetime.now()
        elapsed = endTime - beginTime
        print("Elapsed Time:", elapsed)  # Record elapsed time for reporting

    def simulate(self):
        for _ in range(100):
                self.db.connect()  # Connect to the database
                self.db.set_transaction_isolation_level()  # Set transaction isolation level

                if random.random() < 0.5:
                    self.read_data("20110101", "20111231")

                if random.random() < 0.5:
                    self.read_data("20120101", "20121231")

                if random.random() < 0.5:
                    self.read_data("20130101", "20131231")

                if random.random() < 0.5:
                    self.read_data("20140101", "20141231")

                if random.random() < 0.5:
                    self.read_data("20150101", "20151231")

                self.db.commit()
                self.db.disconnect()

    def read_data(self, begin_date, end_date):
        try:
            result = self.db.select_sales_order_detail(begin_date, end_date)
            print(result)
        except Exception as e:
            print("Error occurred while reading data from the database:")