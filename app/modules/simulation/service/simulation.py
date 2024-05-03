import threading
import random
from modules.simulation.service.users import AUser, BUser

class Simulation():

    @staticmethod
    def start(a_amount, b_amount):
        a_users = [AUser() for _ in range(a_amount)]
        b_users = [BUser() for _ in range(b_amount)]
        
        total_list = a_users + b_users
        random.shuffle(total_list)

        threads = []
        for user_obj in total_list:
            thread = threading.Thread(target=user_obj.start)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
