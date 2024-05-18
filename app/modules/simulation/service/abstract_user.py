from abc import ABC, abstractmethod
from threading import Thread
from modules.database.db_proxy import DBProxy

class IUser(ABC):
    @abstractmethod
    def simulate(self):
        pass

class User(IUser, Thread):

    def __init__(self, name: str, db: DBProxy, transaction_count: int) -> None:
        """User for simulation

        Args:
            name (str): Name of the thraed user
            db (DBProxy): Database proxy object
            transaction_count (int): Number of transactions to simulate
        """

        super().__init__(name=name)
        self.name = name
        self.db = db
        self._transaction_count = transaction_count
        self._elapsed_time = 0

    def run(self):
        raise NotImplementedError("Override the run method for user simulation")

    def simulate(self):
        raise NotImplementedError("Implement the method for user simulation")

    @property
    def elapsed_time(self) -> float:
        return self._elapsed_time
    
    @elapsed_time.setter
    def elapsed_time(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Elapsed time must be a number")
        self._elapsed_time = value

    @property
    def encountered_deadlock_num(self) -> int:
        return self.db._encountered_deadlock_num