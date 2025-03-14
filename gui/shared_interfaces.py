import tkinter as tk
from tkinter import messagebox
import utils
from utils import verificaUser




def on_click_login():
    username = entry_username.get()
    password = entry_password.get()

    if utils.verificaUser(username, password, "../users/user_data.bin"):
        messagebox.showinfo("Login", "Login bem sucedido")
    else:
        label_status.config(text="Usuário ou senha incorretos.", fg="red")

root = tk.Tk() # Cria a janela principal
root.title("Login") # Define o título da janela
root.geometry("300x200") # Define o tamanho da janela

label_username = tk.Label(root, text="Username: ")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Senha:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")  # Mostra '*' no lugar dos caracteres da senha
entry_password.pack(pady=5)


button_login = tk.Button(root, text="Login", command=on_click_login)
button_login.pack(pady=10)


label_status = tk.Label(root, text="", fg="red")
label_status.pack(pady=5)


root.mainloop()