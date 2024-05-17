from modules.database.enums import IsolationLevel
import os
from dotenv import load_dotenv

load_dotenv()

__all__ = ['SERVER', 'DATABASE', 'ISOLATION_LEVEL']

# GUI Configuration


# DB Config
SERVER = os.getenv('SERVER_NAME')
DATABASE = os.getenv('DATABASE_NAME')

# Set a isolation level for simulation 
ISOLATION_LEVEL = IsolationLevel.READ_COMMITTED