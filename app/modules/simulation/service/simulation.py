from config import DATABASE, SERVER, ISOLATION_LEVEL

from modules.database.db_proxy import DBProxy
from modules.simulation.service.users import AUser, BUser

import datetime
import threading
import random

class Simulation():

    @classmethod
    def start(cls, a_user_num, b_user_num):
        """Starts the simulation"""
        start = datetime.datetime.now()

        users = cls.generate_users(a_user_num, b_user_num)

        threads = []
        for user in users:
            thread = threading.Thread(target=user.start)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_duration = datetime.datetime.now() - start
        return total_duration
    

    @classmethod
    def generate_users(cls, a_user_num, b_user_num):
        """Generates the users"""

        a_users = []
        for _ in range(a_user_num):
            db = DBProxy(SERVER, DATABASE, ISOLATION_LEVEL)
            a_users.append(AUser(db))

        b_users = []
        for _ in range(b_user_num):
            db = DBProxy(SERVER, DATABASE, ISOLATION_LEVEL)
            b_users.append(BUser(db))
        
        users = a_users + b_users

        # return random shuffled user list
        random.shuffle(users)
        return users
    
