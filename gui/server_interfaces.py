import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import utils
from server import Server
from client import Client



class App(tk.Tk):
    def __init__(self, title, size):

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        self.loginMenu = LoginMenu(self)
        self.loginMenu.pack(expand=True, fill="both")
        # widgets



        # run
        self.mainloop()

    def switch_to_service_menu(self):
        # Remove the Menu frame
        self.loginMenu.pack_forget()

        # Create and pack the MainApp frame
        self.service_menu = ServiceMenu(self)
        self.service_menu.pack(expand=True, fill="both")


class LoginMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()


    def create_widgets(self):

        self.label_username = tk.Label(self, text="Username: ")
        self.label_username.pack(pady=5)

        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(self, text="Senha:")
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(self, show="*")  # Mostra '*' no lugar dos caracteres da senha
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.on_click_login)
        self.button_login.pack(pady=10)

        self.label_status = tk.Label(self, text="", fg="red")
        self.label_status.pack(pady=5)


    def on_click_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if utils.verificaUser(username, password, "../users/user_data.bin"):
            messagebox.showinfo("Login", "Login bem sucedido!")
            self.parent.switch_to_service_menu()
        else:
            self.label_status.config(text="Usuário ou senha incorretos.", fg="red")


class ServiceMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()


    def create_widgets(self):
        self.button_startClient = tk.Button(self, text="Start Client", command=self.on_click_client)
        self.button_startClient.pack(pady=10)

        self.button_startServer = tk.Button(self, text="Start Server", command=self.on_click_server)
        self.button_startServer.pack(pady=10)
        self.button_startServer.config(background="orange")

    def on_click_server(self):
        server = Server(host='127.0.0.1', port=12345)
        try:
            # Inicia o servidor
            server.start()
        except KeyboardInterrupt:
            # Encerra o servidor ao pressionar Ctrl+C
            server.stop()

    def on_click_client(self):
        client = Client(host='127.0.0.1', port=12345)
        client.connect()



App("MyFTP", (600, 300))