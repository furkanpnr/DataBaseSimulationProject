from modules.simulation.service.simulation import Simulation
import customtkinter


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Topics Simulator Midterm Project")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")
        self.geometry("1000x600")

        #Input Fields
        self.frame1 = customtkinter.CTkFrame(self)
        self.frame1.pack(padx=20, pady=20)

        a_label = customtkinter.CTkLabel(self.frame1, text="A user Amount", fg_color="transparent")
        a_label.grid(row=0, column=0,padx=20, pady=0)

        self.a_user_amount = customtkinter.CTkEntry(self.frame1, placeholder_text="1")
        self.a_user_amount.grid(row=0, column=1,padx=20, pady=20)

        b_label = customtkinter.CTkLabel(self.frame1, text="B user Amount", fg_color="transparent")
        b_label.grid(row=1, column=0,padx=20, pady=20)


        self.b_user_amount = customtkinter.CTkEntry(self.frame1, placeholder_text="1")
        self.b_user_amount.grid(row=1, column=1,padx=20, pady=20)


        isolation_level_label = customtkinter.CTkLabel(self.frame1, text="Isolation Level (1-5)", fg_color="transparent")
        isolation_level_label.grid(row=2, column=0,padx=20, pady=20)


        self.isolation_level_amount = customtkinter.CTkEntry(self.frame1, placeholder_text="1")
        self.isolation_level_amount.grid(row=2, column=1,padx=20, pady=20)

        #Buttons
        self.button = customtkinter.CTkButton(self, text="Start Simulation", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

        # self.button1 = customtkinter.CTkButton(self, text="my button", command=self.button1_callbck)
        # self.button1.pack(padx=20, pady=20)

        #Output Fields (Number of Type A Users, Number of Type B Users, Number of Deadlocks Encountered by Type A Users, Average Duration of Type B Threads, Number of Deadlocks Encountered by Type B Users)
        self.output_container = customtkinter.CTkFrame(self, width=1000, height=500, bg_color="transparent")
        self.output_container.pack(padx=20, pady=20)

        

        self.number_of_type_a_users_label = customtkinter.CTkLabel(self.output_container, text="A User Amount", fg_color="transparent")
        self.number_of_type_a_users_label.grid(row=0, column=0, padx=20, pady=5)

        self.number_of_type_a_users = customtkinter.CTkLabel(self.output_container, text="", fg_color="transparent")
        self.number_of_type_a_users.grid(row=1, column=0, padx=20, pady=5)

        
        self.number_of_type_b_users_label = customtkinter.CTkLabel(self.output_container, text="B User Amount", fg_color="transparent")
        self.number_of_type_b_users_label.grid(row=0, column=1, padx=20, pady=5)

        self.number_of_type_b_users = customtkinter.CTkLabel(self.output_container, text="", fg_color="transparent")
        self.number_of_type_b_users.grid(row=1, column=1, padx=20, pady=5)


        self.number_of_deadlocks_a_label = customtkinter.CTkLabel(self.output_container, text=" A DeadLock Amount", fg_color="transparent")
        self.number_of_deadlocks_a_label.grid(row=0, column=2, padx=20, pady=5)

        self.number_of_deadlocks_a = customtkinter.CTkLabel(self.output_container, text="", fg_color="transparent")
        self.number_of_deadlocks_a.grid(row=1, column=2, padx=20, pady=5)


        self.number_of_deadlocks_b_label = customtkinter.CTkLabel(self.output_container, text="B DeadLock Amount", fg_color="transparent")
        self.number_of_deadlocks_b_label.grid(row=0, column=3, padx=20, pady=5)

        self.number_of_deadlocks_b = customtkinter.CTkLabel(self.output_container, text="", fg_color="transparent")
        self.number_of_deadlocks_b.grid(row=1, column=3, padx=20, pady=5)


        self.average_duration_b_label = customtkinter.CTkLabel(self.output_container, text="Elapsed Time", fg_color="transparent")
        self.average_duration_b_label.grid(row=0, column=4, padx=20, pady=5)

        self.average_duration_b = customtkinter.CTkLabel(self.output_container, text="", fg_color="transparent")
        self.average_duration_b.grid(row=1, column=4, padx=20, pady=5)



        #Logs
        self.frame2 = customtkinter.CTkFrame(self, width=1000, height=500, bg_color="transparent")
        self.frame2.pack(padx=20, pady=20)

        self.output = customtkinter.CTkLabel(self.frame2, width=1000, height=500, text="Output", fg_color="transparent")


    def button_callbck(self):
        a_user_amount = int(self.a_user_amount.get())
        b_user_amount = int(self.b_user_amount.get())
        number_of_deadlocks_a = 0
        number_of_deadlocks_b = 0
        elapsed_time = 0
        elapsed_time = Simulation.start(a_user_amount, b_user_amount)

        self.number_of_type_a_users.configure(text=str(a_user_amount))
        self.number_of_type_b_users.configure(text=str(b_user_amount))
        self.number_of_deadlocks_a.configure(text=str(number_of_deadlocks_a))
        self.number_of_deadlocks_b.configure(text=str(number_of_deadlocks_b))
        self.average_duration_b.configure(text=elapsed_time)

        # pass

    def button1_callbck(self):
        print("button1 clicked")
        # Simulation.get_query()
