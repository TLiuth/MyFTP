import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

sys.path.append('../')
from server import Server
from client import Client
import threading
from . import client_interfaces


class ServiceMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.ip = ""

    def create_widgets(self):
        # Expande para preencher o espaço e permitir centralização
        self.pack(expand=True, fill="both")

        # Frame para os widgets do server (centraliza)
        self.frame = tk.Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona no centro

        self.button_startClient = tk.Button(self.frame, text="Start Client", command=self.on_click_client_verify_login,
                                            width=10, height=2)
        self.button_startClient.pack(pady=10)
        self.button_startClient.config(state=tk.ACTIVE)

        self.button_startServer = tk.Button(self.frame, text="Start Server", command=self.on_click_server, width=10,
                                            height=2)
        self.button_startServer.pack(pady=10)
        self.button_startServer.config(background="orange")

        self.entry_ip = tk.Entry(self.frame, background="orange")
        self.entry_ip.insert(0, '127.0.0.1')
        self.entry_ip.pack(pady=5)

    def on_click_server(self):
        try:
            # Inicia o servidor
            ip = self.entry_ip.get()
            self.server = Server(host=f'{ip}', port=12345)
            server_thread = threading.Thread(target=self.server.start, daemon=True)
            server_thread.start()

            self.label_iniciado = tk.Label(self.frame, text=f"Server running on {ip}!")
            self.label_iniciado.pack(pady=10)
            self.button_stopServer = tk.Button(self.frame, text="Stop Server", background="red",
                                               command=self.on_click_stop_server)
            self.button_stopServer.pack(pady=10)

            # bloqueia o botão de iniciar server e cliente
            self.button_startServer.config(state=tk.DISABLED)
            self.button_startClient.config(state=tk.DISABLED)
        except Exception as e:
            # Handle any errors that occur while starting the server
            messagebox.showerror("Server Error", f"Failed to start server: {e}")

    def on_click_client(self):
        ip = self.ip
        client = Client(host=f"{ip}", port=12345)
        client.connect()
        self.pack_forget()  # Hide the ServiceMenu
        self.client_menu = client_interfaces.ClientMenu(self.master, client)
        self.client_menu.pack(expand=True, fill="both")

    def on_click_client_verify_login(self):
        # Guarda IP para uso posterior
        self.ip = self.entry_ip.get()
        self.pack_forget()  # Hide the ServiceMenu

        # Create the LoginMenu with a callback to handle successful login
        self.login_menu = client_interfaces.LoginMenu(self.master, on_login_success=self.on_click_client)
        self.login_menu.pack(expand=True, fill="both")

    def on_click_stop_server(self):
        self.server.stop()
        self.label_iniciado.pack_forget()
        self.button_stopServer.pack_forget()

        self.button_startServer.config(state=tk.NORMAL)
        self.button_startClient.config(state=tk.NORMAL)

        messagebox.showinfo("Server", "Servidor encerrado!")
        exit(1)