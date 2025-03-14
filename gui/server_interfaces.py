import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from server import Server
from client import Client
import threading



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

        self.entry_ip = tk.Entry(self, background="orange")  # Mostra '*' no lugar dos caracteres da senha
        self.entry_ip.insert(0, '127.0.0.1')
        self.entry_ip.pack(pady=5)

    def on_click_server(self):

        try:
            # Inicia o servidor
            ip = self.entry_ip.get()
            self.server = Server(host=f'{ip}', port=12345)
            server_thread = threading.Thread(target=self.server.start, daemon=True)
            server_thread.start()

            self.label_iniciado = tk.Label(self, text=f"Server running on {ip}!")
            self.label_iniciado.pack(pady=10)
            self.button_stopServer = tk.Button(self, text="Stop Server", background="red", command=self.on_click_stop_server)
            self.button_stopServer.pack(pady=10)

            # bloqueia o botão de iniciar server ou de iniciar cliente
            self.button_startServer.config(state=tk.DISABLED)
            self.button_startClient.config(state=tk.DISABLED)
        except Exception as e:
            # Handle any errors that occur while starting the server
            messagebox.showerror("Server Error", f"Failed to start server: {e}")


    def on_click_client(self):
        client = Client(host='127.0.0.1', port=12345)
        client.connect()

    def on_click_stop_server(self):

        self.server.stop()
        self.label_iniciado.pack_forget()
        self.button_stopServer.pack_forget()

        self.button_startServer.config(state=tk.NORMAL)
        self.button_startClient.config(state=tk.NORMAL)

        messagebox.showinfo("Server", "Servidor encerrado!")
        exit(1)



