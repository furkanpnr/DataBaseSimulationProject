import threading
import random
from modules.simulation.service.users import AUser, BUser
from modules.database.db_proxy import DBProxy
from config import DATABASE,SERVER

class Simulation():

    @staticmethod
    def start(a_amount, b_amount):
        mydb = DBProxy(SERVER,DATABASE)
        a_users = [AUser(mydb) for _ in range(a_amount)]
        b_users = [BUser(mydb) for _ in range(b_amount)]
        
        total_list = a_users + b_users
        random.shuffle(total_list)

        threads = []
        for user_obj in total_list:
            thread = threading.Thread(target=user_obj.start)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
