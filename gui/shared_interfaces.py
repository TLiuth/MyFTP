import tkinter as tk
import sys
sys.path.append('../')

from . import server_interfaces

class App(tk.Tk):
    def __init__(self, title, size):
        # Main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        # Start with the ServiceMenu
        self.service_menu = server_interfaces.ServiceMenu(self)
        self.service_menu.pack(expand=True, fill="both")

        # Run the application
        self.mainloop()

#App("MyFTP", (800, 500))