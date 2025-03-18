import tkinter as tk
from tkinter import messagebox, ttk
import sys
sys.path.append('../')
import utils
import server_interfaces

class App(tk.Tk):
    def __init__(self, title, size):

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        # self.loginMenu = LoginMenu(self)
        # self.loginMenu.pack(expand=True, fill="both")
        self.service_menu = server_interfaces.ServiceMenu(self)
        self.service_menu.pack(expand=True, fill="both")

        # widgets


        # run
        self.mainloop()

    def switch_to_service_menu(self):
        # Remove the Menu frame
        self.loginMenu.pack_forget()

        # Create and pack the MainApp frame
        self.service_menu = server_interfaces.ServiceMenu(self)
        self.service_menu.pack(expand=True, fill="both")


class LoginMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()


    def create_widgets(self):
        # Expande para preencher o espaço e permitir centralização
        self.pack(expand=True, fill="both")

        # Frame para os widgets do login (centraliza)
        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona no centro

        self.label_username = tk.Label(frame, text="Username: ")
        self.label_username.pack(pady=5)

        self.entry_username = tk.Entry(frame)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(frame, text="Senha:")
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(frame, text="Login", command=self.on_click_login)
        self.button_login.pack(pady=10)

        self.label_status = tk.Label(frame, text="", fg="red")
        self.label_status.pack(pady=5)
        
    def on_click_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if utils.verificaUser(username, password, "../users/user_data.bin"):
            messagebox.showinfo("Login", "Login bem sucedido!")
            self.parent.switch_to_service_menu()
        else:
            self.label_status.config(text="Usuário ou senha incorretos.", fg="red")


App("MyFTP", (800, 500))