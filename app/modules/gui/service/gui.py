import customtkinter
from modules.simulation.service.simulation import Simulation

class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Topics Simulator Midterm Project")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")
        self.geometry("800x600")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

        self.button1 = customtkinter.CTkButton(self, text="my button", command=self.button1_callbck)
        self.button1.pack(padx=20, pady=20)
        

    def button_callbck(self):
        Simulation.start(0,5)

    def button1_callbck(self):
        print("button1 clicked")
        Simulation.get_query()

