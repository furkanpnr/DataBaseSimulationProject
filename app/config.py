from modules.database.enums import IsolationLevel

__all__ = ['SERVER', 'DATABASE', 'ISOLATION_LEVEL']

# GUI Configuration


# DB Config
SERVER = 'LENOVO\SQLEXPRESS'
DATABASE = 'AdventureWorks2019'

# Set a isolation level for simulation 
ISOLATION_LEVEL = IsolationLevel.READ_COMMITTED