from modules.database.db_proxy import DBProxy

__all__ = ['_db_proxy']

# GUI Configuration


# DB Config
SERVER = '<server_name>'
DATABASE = '<database_name>'


_db_proxy = DBProxy(SERVER, DATABASE)