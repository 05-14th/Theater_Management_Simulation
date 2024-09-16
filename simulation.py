import simpy
import random
import statistics
import tkinter as tk
from tkinter import PhotoImage, Toplevel, messagebox

wait_times = []

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Theater Simulation")
        self.attributes("-fullscreen", True)
        self.resizable(True, True)
        self.bind('<Escape>', self.quitFullscreen)
        self.bind('<F11>', self.toggleFullscreen)
        self.initializeUI()

    def quitFullscreen(self, event=None):
        self.attributes('-fullscreen', False)
        self.geometry('800x600')

    def toggleFullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))
        self.geometry("800x600")
        return "break"
    
    def initializeUI(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=0)

        self.headerFrame = tk.Frame(self, bg="lightblue", height=100)
        self.headerFrame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.headerFrame.grid_propagate()

        self._title = tk.Label(self.headerFrame, text="Theater Simulation", fg="black", bg="lightblue", font=("Arial", 20))
        self._title.pack(side=tk.LEFT, padx=10, pady=10)

        self.mainFrame = tk.Frame(self, bg="gray")
        self.mainFrame.grid(row=1, column=0, rowspan=4, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.tableFrame = tk.Frame(self.mainFrame)
        self.tableFrame.grid(row=0, column=0, sticky="nsew")
        self.suggestionFrame = tk.Frame(self.mainFrame)
        self.suggestionFrame.grid(row=0, column=1, sticky="nsew")

        column_names = ["Number of Cashiers", "Number of Servers", "Number of Ushers", "Total Cost","Waiting Time"]
        self.t = Table(self.tableFrame, column_names)

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.buttonFrame.grid_rowconfigure(0, weight=1)
        self.buttonFrame.grid_columnconfigure(0, weight=1)
        self.buttonFrame.grid_columnconfigure(1, weight=1)
        self.buttonFrame.grid_columnconfigure(2, weight=1)

        self.bg_image_settings = PhotoImage(file="Icons/settings.png")
        self.settingsButton = tk.Button(self.buttonFrame, command=self.openControlScreen, image=self.bg_image_settings, compound="center", border=1, width=300)
        self.settingsButton.grid(row=0, column=0, sticky="nsew")

        self.bg_image_play = PhotoImage(file="Icons/play.png")
        self.suggestButton = tk.Button(self.buttonFrame, command=self.openSuggestionBox, image=self.bg_image_play, compound="center", border=1, width=300)
        self.suggestButton.grid(row=0, column=1, sticky="nsew")

        self.bg_image_exit = PhotoImage(file="Icons/exit.png")
        self.exitButton = tk.Button(self.buttonFrame, command=self.quit, image=self.bg_image_exit, compound="center", border=1, width=300)
        self.exitButton.grid(row=0, column=2, sticky="nsew")

    def openControlScreen(self):
        self.settingsButton["state"] = tk.DISABLED
        control_screen = ControlScreen(self, self.update_table)
        self.wait_window(control_screen)
        self.settingsButton["state"] = tk.NORMAL
       
    def update_table(self, results):
        num_cashiers, num_servers, num_ushers, total_cost, wait_time = results
        self.t.add_row((num_cashiers, num_servers, num_ushers, total_cost,wait_time))

    def openSuggestionBox(self):
        self.suggestButton["state"] = tk.DISABLED
        suggestion_screen = Suggestions(self, self.update_list)
        self.wait_window(suggestion_screen)
        self.suggestButton["state"] = tk.NORMAL

    def update_list(self):
        pass

class ControlScreen(Toplevel):
    def __init__(self,parent,update_table_callback):
        super().__init__(parent)
        self.title("Edit Variables")
        self.geometry("380x250")
        self.resizable(False, False)
        self.update_table_callback = update_table_callback
        self.create_UI()

    def create_UI(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.cashier_label = tk.Label(self, text="Number of Cashier Working:")
        self.cashier_label.grid(row=1, column=0, sticky="ew", pady=5)
        self.cashierNum = tk.Entry(self)
        self.cashierNum.grid(row=1, column=1, sticky="ew")
        self.servers_label = tk.Label(self, text="Number of Servers Working:")
        self.servers_label.grid(row=2, column=0, sticky="ew", pady=5)
        self.serverNum = tk.Entry(self)
        self.serverNum.grid(row=2, column=1, sticky="ew", pady=5)
        self.usher_label = tk.Label(self, text="Number of Ushers:")
        self.usher_label.grid(row=3, column=0, sticky="ew", pady=5)
        self.usherNum = tk.Entry(self)
        self.usherNum.grid(row=3, column=1, sticky="ew", pady=5)
        self.cashierCost_label = tk.Label(self, text="Cost per Cashier: ")
        self.cashierCost_label.grid(row=4, column=0, sticky="ew", pady=5)
        self.cashierCost = tk.Entry(self)
        self.cashierCost.grid(row=4, column=1, sticky="ew", pady=5)
        self.serverCost_label = tk.Label(self, text="Cost per Server: ")
        self.serverCost_label.grid(row=5, column=0, sticky="ew", pady=5)
        self.serverCost = tk.Entry(self)
        self.serverCost.grid(row=5, column=1, sticky="ew", pady=5)
        self.usherCost_label = tk.Label(self, text="Cost per Usher: ")
        self.usherCost_label.grid(row=6, column=0, sticky="ew", pady=5)
        self.usherCost = tk.Entry(self)
        self.usherCost.grid(row=6, column=1, sticky="ew", pady=5)
        
        self.button = tk.Button(self, text="Save", command=self.run_simulation, compound="center", border=1, width=50, height=2)
        self.button.grid(row=7,columnspan=2, pady=15)

    def get_user_input(self):
        num_cashiers = self.cashierNum.get()
        num_servers = self.serverNum.get()
        num_ushers = self.usherNum.get()
        params = [num_cashiers, num_servers, num_ushers]
        if all(str(i).isdigit() for i in params): # Check input is valid 
            params = [int(x) for x in params]
        else:
            print(
                "Could not parse input. Simulation will use default values:",
                "\n1 cashier, 1 server, 1 usher.",
                )
            params = [1, 1, 1]
        return params
    
    def go_to_movies(self, env, moviegoer, theater):
        # Moviegoer arrives at the theater
        arrival_time = env.now
        with theater.cashier.request() as request:
            yield request
            yield env.process(theater.purchase_ticket(moviegoer))
            
        with theater.usher.request() as request:
            yield request
            yield env.process(theater.check_ticket(moviegoer))
        
        if random.choice([True, False]):
            with theater.server.request() as request:
                yield request
                yield env.process(theater.sell_food(moviegoer))
 
        # Moviegoer heads into the theater
        wait_times.append(env.now - arrival_time)

    def run_theater(self, env, num_cashiers, num_servers, num_ushers):
        theater = Theater(env, num_cashiers, num_servers, num_ushers)
        for moviegoer in range(3):
            env.process(self.go_to_movies(env, moviegoer, theater))
    
        while True:
            yield env.timeout(0.20) # Wait a bit before generating a new person
            moviegoer += 1
            env.process(self.go_to_movies(env, moviegoer, theater))

    def get_average_wait_time(self, wait_times):
        average_wait = statistics.mean(wait_times)
        # Pretty print the results
        minutes, frac_minutes = divmod(average_wait, 1)
        seconds = frac_minutes * 60
        return round(minutes), round(seconds)
    
    def run_simulation(self):
        # Setup
        random.seed(42)
        num_cashiers, num_servers, num_ushers = self.get_user_input()
        # Run the simulation
        env = simpy.Environment()
        env.process(self.run_theater(env, num_cashiers, num_servers, num_ushers))
        env.run(until=90)
        # View the results
        mins, secs = self.get_average_wait_time(wait_times)
        cs = self.cashierCost.get()
        sc = self.serverCost.get()
        uc = self.usherCost.get()
        total_cost = ((int(num_cashiers) *  int(cs)) + (int(num_servers) * int(sc)) + (int(num_ushers) * int(uc)))
        results = (num_cashiers, num_servers, num_ushers, total_cost, f"{mins} min and {secs} sec")
        wait_times.clear()
        if self.update_table_callback:
            self.update_table_callback(results)
        self.destroy()

class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)
        
    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))
        
    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)
        
    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 5))

class Table:
    def __init__(self, parent,columns):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.table = []
        self.create_table(columns)

    def create_table(self, column_names):
        self.table = []
        header_row = tk.Frame(self.frame)
        header_row.pack(fill=tk.X)
        for col, name in enumerate(column_names):
            cell = tk.Label(header_row, text=name, borderwidth=1, relief="solid", width=15, height=2, bg="lightgray")
            cell.grid(row=0, column=col, sticky="nsew")
            self.table.append(cell)
        
        self.data_rows = []
        self.frame.grid_rowconfigure(0, weight=0)
        self.row_count = 1

    def add_row(self, row_data):
        row = tk.Frame(self.frame)
        row.pack(fill=tk.X)
        self.data_rows.append(row)
        for col, data in enumerate(row_data):
            cell = tk.Label(row, text=data, borderwidth=1, relief="solid", width=15, height=2)
            cell.grid(row=0, column=col, sticky="nsew")
        self.frame.grid_rowconfigure(self.row_count, weight=1)
        self.row_count += 1

class Suggestions(Toplevel):
    def __init__(self, parent, update_suggestions_callback):
        super().__init__(parent)
        self.title("Suggestions")
        self.geometry("380x250")
        self.resizable(False, False)
        self.update_suggestions_callback = update_suggestions_callback
        self.initUI()

    def initUI(self):
        self.grid_columnconfigure(0, weight=1)
        
        self.suggestionBox = tk.Text(self)
        self.suggestionBox.grid(row=0, column=0)
    
if __name__ == "__main__":
    root = MainScreen()
    root.mainloop()