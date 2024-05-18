from modules.simulation.service.simulation import Simulation
import tkinter
import tkinter.messagebox
import customtkinter

from modules.database.enums import IsolationLevel
from threading import Thread


customtkinter.set_appearance_mode("Dark")  # Modes: "Light", "Dark", "System" (DEFAULT: "Dark")
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Gui(customtkinter.CTk):
    def __init__(self, 
                 height: int, 
                 width: int, 
                 resizeable: bool, 
                 title: str, 
                 info: str):
        super().__init__()

        # Configure the window
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(width=resizeable, height=resizeable)

        self.label_font = customtkinter.CTkFont(size=12, weight="bold")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)  # Make the center column expandable
        self.grid_columnconfigure((2, 3), weight=0)  # Make the right column fixed
        self.grid_rowconfigure((0, 1, 2), weight=1)  # Make the top row expandable

        # Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # logo label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulator App", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # A User Count label and entry
        self.a_user_count_label = customtkinter.CTkLabel(self.sidebar_frame, 
                                                         text="A User Count:", 
                                                         font=self.label_font,
                                                         anchor="w")
        self.a_user_count_label.grid(row=1, column=0, padx=25, pady=10, sticky="w")
        self.a_user_count_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Enter a number")
        self.a_user_count_entry.grid(row=2, column=0, padx=20, pady=10)

        # B User Count label and entry
        self.b_user_count_label = customtkinter.CTkLabel(self.sidebar_frame, 
                                                         text="B User Count:", 
                                                         font=self.label_font,
                                                         anchor="w")
        self.b_user_count_label.grid(row=3, column=0, padx=25, pady=10, sticky="w")
        self.b_user_count_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Enter a number")
        self.b_user_count_entry.grid(row=4, column=0, padx=20, pady=10)

        # Iso Level label and OptionMenu
        self.iso_level_label = customtkinter.CTkLabel(self.sidebar_frame, 
                                                      text="Isolation Level:",
                                                      font=self.label_font, 
                                                      anchor="w")
        self.iso_level_label.grid(row=5, column=0, padx=25, pady=10, sticky="w")
        self.iso_level_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, 
                                    values=["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"])
        self.iso_level_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Start Simulation button
        self.start_button = customtkinter.CTkButton(self.sidebar_frame, 
                                                    text="Start",
                                                    font=self.label_font, 
                                                    command=self.start_simulation)
        self.start_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10)

        # Appearance Mode label and OptionMenu
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 10))

        # Info box
        self.info_box = customtkinter.CTkTextbox(self, 
                                                 height=250, 
                                                 corner_radius=10, 
                                                 border_width=1, 
                                                 font=customtkinter.CTkFont(size=15), 
                                                 wrap="word")
        self.info_box.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.info_box.insert("0.0", info)

        # Result table frame
        self.result_table_frame = customtkinter.CTkFrame(self, 
                                                         corner_radius=10, 
                                                         border_width=1,
                                                         )
        self.result_table_frame.grid(row=2, column=1, padx=20, pady=20)

        # Result table title
        self.result_label = customtkinter.CTkLabel(self.result_table_frame, 
                                                text="Simulation Results", 
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        self.result_label.grid(row=0, column=0, columnspan=6, pady=10)

        # Result table headers and values
        column_titles = [
            "Number of Type A Users", 
            "Number of Type B Users", 
            "Average Duration of Type A Threads", 
            "Number of Deadlocks Encountered by Type A Users", 
            "Average Duration of Type B Threads", 
            "Number of Deadlocks Encountered by Type B Users"
        ]
        self.result_labels = []

        for col, title in enumerate(column_titles):
            header_frame = customtkinter.CTkFrame(self.result_table_frame, 
                                                  border_width=1, 
                                                  corner_radius=10, 
                                                  width= self.result_table_frame.winfo_width() // len(column_titles))
            header_frame.grid(row=1, column=col, padx=10, pady=10, sticky="nsew")

            header_label = customtkinter.CTkLabel(header_frame, 
                                                  text=title, 
                                                  font=self.label_font, 
                                                  anchor="center", 
                                                  wraplength=140,
                                                  padx=10, pady=10)
            header_label.pack(fill="both", expand=True)

            value_frame = customtkinter.CTkFrame(self.result_table_frame, 
                                                 border_width=1, 
                                                 corner_radius=10,
                                                 width=self.result_table_frame.winfo_width() // len(column_titles))
            value_frame.grid(row=2, column=col, padx=10, pady=10, sticky="nsew")

            value_label = customtkinter.CTkLabel(value_frame, 
                                                 text="N/A", 
                                                 font=self.label_font, 
                                                 anchor="center", 
                                                 wraplength=140,
                                                 padx=10, pady=10)
            value_label.pack(fill="both", expand=True)
            self.result_labels.append(value_label)


    def update_result_table(self, data: dict):
        """Update the result table with new data."""
        for i, key in enumerate(data):
            self.result_labels[i].configure(text=str(data[key]))


    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode of the application."""
        customtkinter.set_appearance_mode(new_appearance_mode)
   
    def _validate_input(self):
        """Validate the input values."""
        a_user_count = self.a_user_count_entry.get()
        b_user_count = self.b_user_count_entry.get()
        iso_level = self.iso_level_optionmenu.get()

        # validate the input values not to be empty
        if not a_user_count or not b_user_count:
            tkinter.messagebox.showerror("Error", "Please fill the required fields")
            return

        # validate the input values to be integers
        try:
            a_user_count = int(a_user_count)
            b_user_count = int(b_user_count)
        except ValueError:
            tkinter.messagebox.showerror("Error", "Please enter valid numbers")
            return
        
        # isolation level validation
        try:
            isolation_level = IsolationLevel(iso_level.upper())
        except ValueError:
            tkinter.messagebox.showerror("Error", "Invalid Isolation Level")
            return

        return a_user_count, b_user_count, isolation_level


    def start_simulation(self):
        """Simulate the transactions with the given parameters.
        """

        # Validate the input values
        a_user_count, b_user_count, isolation_level = self._validate_input()
        
        # # Simulation runner thread
        # simulation_thread = Thread(target=Simulation.start,
        #                             args=(a_user_count, b_user_count, 2, isolation_level))
        
        # simulation_thread.start()
        # simulation_thread.join()

        results = Simulation.start(
            a_user_count=a_user_count,
            b_user_count=b_user_count,
            transaction_count=2,
            isolation_lvl=isolation_level
        )
        self.update_result_table(results)