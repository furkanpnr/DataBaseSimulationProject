from modules.simulation.service.users import AUser, BUser
from modules.database.db_proxy import DBProxy
from modules.database.enums import IsolationLevel
from config import SERVER, DATABASE

import time
import random

from rich.console import Console
from rich.table import Table


class Simulation():

    @classmethod
    def start(cls, 
              a_user_count: int, 
              b_user_count: int,
              transaction_count: int,
              isolation_lvl: IsolationLevel):
        
        """Starts the transaction simulation on the database

        Args:
            a_user_count (int): Number of A users
            b_user_count (int): Number of B users
            transaction_count (int): Number of transactions per user
            isolation_lvl (str): Isolation level to be set for the transactions
        """
        users = cls.generate_users(a_user_count, b_user_count, transaction_count, isolation_lvl)

        
        print("[bold green] Starting simulation \n")
        begin_time = time.time()

        for user in users:
            user.start()
        
        for user in users:
            user.join()
        
        end_time = time.time()
        print("[bold cyan] All users finished")
        print(f"[bold]Simulation took {end_time - begin_time:.2f} seconds \n")

        a_users = [user for user in users if isinstance(user, AUser)]
        b_users = [user for user in users if isinstance(user, BUser)]

        avg_a_user_time = sum([user.elapsed_time for user in a_users]) / len(a_users) if len(a_users) > 0 else 0
        avg_b_user_time = sum([user.elapsed_time for user in b_users]) / len(b_users) if len(b_users) > 0 else 0

        a_user_deadlocks = sum([user.encountered_deadlock_num for user in a_users])
        b_user_deadlocks = sum([user.encountered_deadlock_num for user in b_users])

        cls._print_result(a_users, b_users, avg_a_user_time, a_user_deadlocks, avg_b_user_time, b_user_deadlocks)

        results = {
            "a_user_count": len(a_users),
            "b_user_count": len(b_users),
            "avg_a_user_time": f"{avg_a_user_time:.2f} s",
            "a_user_deadlocks": a_user_deadlocks,
            "avg_b_user_time": f"{avg_b_user_time:.2f} s",
            "b_user_deadlocks": b_user_deadlocks
        }
        return results
    

    @classmethod
    def generate_users(cls, 
                       a_user_count: int, 
                       b_user_count: int,
                       transaction_count: int,
                       isolation_lvl: IsolationLevel):
        
        """Generates users

        Args:
            a_user_count (int): Number of A users
            b_user_count (int): Number of B users
            transaction_count (int): Number of transactions per user
            isolation_lvl (IsolationLevel): Isolation level to be set for the transactions

        Returns:
            list: List of users to be simulated
        """

        users = []

        for i in range(a_user_count):
            db = DBProxy(SERVER, DATABASE, isolation_lvl)
            users.append(AUser(name=f"AUser_{i}", db=db, transaction_count=transaction_count))
        
        for i in range(b_user_count):
            db = DBProxy(SERVER, DATABASE, isolation_lvl)
            users.append(BUser(name=f"BUser_{i}", db=db, transaction_count=transaction_count))
        
        random.shuffle(users)
        return users
    

    @classmethod
    def _print_result(cls, 
                      a_users: list, 
                      b_users: list, 
                      avg_a_user_time: float, 
                      a_user_deadlocks: int, 
                      avg_b_user_time: float, 
                      b_user_deadlocks: int):
        
        console = Console()

        # Create a table
        table = Table(title="Simulation Results")
        table.add_column("Number of Type A Users", style="cyan")
        table.add_column("Number of Type B Users", style="magenta")
        table.add_column("Average Duration of Type A Threads", style="cyan")
        table.add_column("Number of Deadlocks Encountered by Type A Users", style="magenta")
        table.add_column("Average Duration of Type B Threads", style="cyan")
        table.add_column("Number of Deadlocks Encountered by Type B Users", style="magenta")

        table.add_row(
            str(len(a_users)),
            str(len(b_users)),
            f"{avg_a_user_time:.2f} s",
            str(a_user_deadlocks),
            f"{avg_b_user_time:.2f} s",
            str(b_user_deadlocks)
        )

        console.print(table)
    
