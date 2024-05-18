import os
from pathlib import Path
from dotenv import load_dotenv

from tools import _path_joiner

load_dotenv()

__all__ = ['SERVER', 'DATABASE', 'WIDTH', 'HEIGHT', 'RESIZEABLE', 'TITLE', 'INFO']


# PATHS
BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = _path_joiner(BASE_PATH, 'data')

#Experiments Paths
EXPERIMENTS_PATH = _path_joiner(DATA_PATH, 'experiments')

READ_COMMITTED_PATH = _path_joiner(EXPERIMENTS_PATH, 'read_committed_experiments.json')
READ_UNCOMMITTED_PATH = _path_joiner(EXPERIMENTS_PATH, 'read_uncommitted_experiments.json')
REPEATABLE_READ_PATH = _path_joiner(EXPERIMENTS_PATH, 'repeatable_read_experiments.json')
SERIALIZABLE_PATH = _path_joiner(EXPERIMENTS_PATH, 'serializable_experiments.json')


# GUI Configuration
WIDTH = 1250
HEIGHT = 600
RESIZEABLE = False
TITLE = "SE 308 Advanced Topics in Database Systems - Term Project"
# Information about the project
INFO = "This project was developed for the SE 308 Advanced Topics in Database Systems course.\n\n" \
       "This application simulates scenarios where multiple users perform transactions on a database simultaneously. " \
       "It is designed to help understand the behavior of database systems under concurrent access, " \
       "illustrating concepts such as transaction isolation levels, deadlocks, and performance metrics.\n\n" \
       "The following individuals contributed to this project:\n" \
       "- Furkan Pınar\n" \
       "- Serhat Çelik\n" \
       "- Metehan Bağcı"

# DB Config
SERVER = os.getenv('SERVER_NAME')
DATABASE = os.getenv('DATABASE_NAME')