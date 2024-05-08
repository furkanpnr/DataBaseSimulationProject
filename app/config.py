from modules.database.db_proxy import DBProxy

__all__ = ['_db_proxy', 'SERVER', 'DATABASE']

# GUI Configuration


# DB Config
SERVER = 'LENOVO\SQLEXPRESS'
DATABASE = 'AdventureWorks2019'


_db_proxy = DBProxy(SERVER, DATABASE)