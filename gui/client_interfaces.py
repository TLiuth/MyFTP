import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
sys.path.append('../')
from server import Server
from client import Client
import threading


class ClientMenu(ttk.Frame):
    def __init__(self,parent, client):
        super().__init__(parent)
        self.client = client
        self.create_widgets()
        
    def create_widgets(self):
        self.label_client = tk.Label(self, text="Client", fg="green", font=("Arial Bold", 20))
        self.label_client.place(x=20, y=5, anchor="nw")  # Canto superior esquerdo

        self.label_server = tk.Label(self, text="Server", fg="orange", font=("Arial Bold", 20))
        self.label_server.place(x=680, y=5, anchor="ne")  # Canto superior direito
        
        self.listbox_client = tk.Listbox(self, height=15)
        self.listbox_client.place(x=0, y=70, anchor="nw")  # Posiciona logo abaixo do Client
        self.listbox_client.insert(0, "pasta_cliente.txt")
        
        self.listbox_server = tk.Listbox(self, height=15)
        self.listbox_server.place(x=699, y=70, anchor="ne")
        self.listbox_server.insert(0, "pasta_server.txt")
        
        # Botões no centro
        self.button_right = tk.Button(self, text="→", font=("Arial", 25), width=4, command=self.move_to_server)
        self.button_right.place(relx=0.5, rely=0.4, anchor="center")

        self.button_left = tk.Button(self, text="←", font=("Arial", 25), width=4, command=self.move_to_client)
        self.button_left.place(relx=0.5, rely=0.6, anchor="center")
        
        
    def move_to_server(self):
        """Simula mover arquivo do Client para o Server"""
        selected = self.listbox_client.curselection()
        if selected:
            item = self.listbox_client.get(selected)
            self.listbox_client.delete(selected)
            self.listbox_server.insert("end", item)
            self.client.send_message("put " + item)
            self.client.receive_message()

    def move_to_client(self):
        """Simula mover arquivo do Server para o Client"""
        selected = self.listbox_server.curselection()
        if selected:
            item = self.listbox_server.get(selected)
            self.listbox_server.delete(selected)
            self.listbox_client.insert("end", item)
            self.client.send_message("get " + item)
            self.client.receive_message()
