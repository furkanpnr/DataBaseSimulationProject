from abc import ABC, abstractmethod
from modules.database.db_proxy import DBProxy

class IUser(ABC):

    @abstractmethod
    def start(self):
        pass

class User(IUser):

    def __init__(self, db: DBProxy) -> None:
        super().__init__()
        self.db = db

    def start(self):
        raise NotImplementedError("Implement the method for User")
    
    def simulate(self):
        raise NotImplementedError("Implement the method for user simulation")
