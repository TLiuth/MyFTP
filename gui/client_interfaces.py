import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  

class ClientMenu(tk.Frame):
    def __init__(self, parent, client):
        super().__init__(parent, bg="#f0f0f0")  # Agora 'bg' funciona        
        self.client = client
        self.load_images()
        self.create_widgets()

    def load_images(self):
        """Carrega e redimensiona imagens para os botões"""
        self.img_right = self.resize_image("../seta_direita.png", 50, 40)
        self.img_left = self.resize_image("../seta_esquerda.png", 50, 40)
        self.img_cd = self.resize_image("../cd_icon.png", 35, 35)
        self.img_cd_up = self.resize_image("../cd_up_icon.png", 35, 35)
        self.img_mkdir = self.resize_image("../mkdir_icon.png", 35, 35)
        self.img_rmdir = self.resize_image("../rmdir_icon.png", 35, 35)

        self.img_client = self.resize_image("../cliente_icon.png", 40, 40)
        self.img_server = self.resize_image("../servidor_icon.png", 30, 30)
            
    def resize_image(self, path, width, height):
        """Redimensiona imagem e retorna um PhotoImage"""
        image = Image.open(path)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def create_widgets(self):
        
        self.label_client_icon = tk.Label(self, image=self.img_client, bg="#f0f0f0")
        self.label_client_icon.place(x=60, y=5)
        self.label_client = tk.Label(self, text="Cliente", font=("Tahoma", 20, "bold"), fg="#333", bg="#f0f0f0")
        self.label_client.place(x=100, y=15, anchor="nw")

        self.label_server_icon = tk.Label(self, image=self.img_server, bg="#f0f0f0")
        self.label_server_icon.place(x=565, y=15, anchor="ne")
        self.label_server = tk.Label(self, text="Servidor", font=("Tahoma", 20, "bold"), fg="#333", bg="#f0f0f0")
        self.label_server.place(x=700, y=15, anchor="ne")

        # Listboxes estilizadas
        self.listbox_client = tk.Listbox(self, height=15, width=30, bg="white", fg="#222", font=("Tahoma", 12))
        self.listbox_client.place(x=20, y=70, anchor="nw")
        self.listbox_client.insert(0, "pasta_cliente.txt")

        self.listbox_server = tk.Listbox(self, height=15, width=30, bg="white", fg="#222", font=("Tahoma", 12))
        self.listbox_server.place(x=780, y=70, anchor="ne")
        self.listbox_server.insert(0, "pasta_server.txt")

        self.entry_label = tk.Label(self, text= "Diretório:", font=("Tahoma",10, "bold"), fg="#333", bg="#f0f0f0")
        self.entry_label.place(x=225, y=460, anchor="nw")
        
        # Campo de entrada para CD
        self.entry_directory = tk.Entry(self, width=20, font=("Tahoma", 12))
        self.entry_directory.place(x=300, y=460, anchor="nw")

        # Botões personalizados com efeito de hover
        button_style = {"bd": 2, "bg": "white", "fg": "white", "activebackground": "#45a049", "font": ("Tahoma", 12, "bold")}
        self.button_cd = tk.Button(self, image=self.img_cd, command=self.command_cd, **button_style)
        self.button_cd.place(x=305, y=400)
        ToolTip(self.button_cd, "Mudar de diretório")

        self.button_cd_up = tk.Button(self, image=self.img_cd_up, command=self.command_cd_up, **button_style)
        self.button_cd_up.place(x=355, y=400)
        ToolTip(self.button_cd_up, "Voltar um diretório")

        self.button_mkdir = tk.Button(self, image=self.img_mkdir, command=self.command_mkdir, **button_style)
        self.button_mkdir.place(x=405, y=400)
        ToolTip(self.button_mkdir, "Criar diretório")

        self.button_rmdir = tk.Button(self, image=self.img_rmdir, command=self.command_rmdir, **button_style)
        self.button_rmdir.place(x=455, y=400)
        ToolTip(self.button_rmdir, "Remover diretório")

        # Mensagem de status mais visível
        self.label_status = tk.Label(self, text="", fg="red", font=("Consolas", 11, "bold"), bg="#f0f0f0")
        self.label_status.place(x=510, y=415)

        # Botões no centro para mover arquivos
        self.button_right = tk.Button(self, image=self.img_right, command=self.move_to_server, **button_style)
        self.button_right.place(relx=0.5, rely=0.4, anchor="center")
        ToolTip(self.button_right, "Enviar arquivo")

        self.button_left = tk.Button(self, image=self.img_left, command=self.move_to_client, **button_style)
        self.button_left.place(relx=0.5, rely=0.6, anchor="center")
        ToolTip(self.button_left, "Requisitar arquivo")

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

    def command_cd(self):
        directory = self.entry_directory.get()
        if directory:
            self.label_status.config(text=f"Mudando para {directory}", fg="green")
            self.client.send_message("cd " + directory)
            self.client.receive_message()
            self.entry_directory.delete(0, tk.END)
        else:
            self.label_status.config(text="Por favor, insira um diretório.", fg="red")

    def command_cd_up(self):
        self.label_status.config(text="Voltando um diretório", fg="green")
        self.client.send_message("cd..")
        self.client.receive_message()
        self.entry_directory.delete(0, tk.END)

    def command_mkdir(self):
        directory = self.entry_directory.get()
        if directory:
            self.label_status.config(text=f"Criando o diretório {directory}", fg="green")
            self.client.send_message("mkdir " + directory)
            self.client.receive_message()
            self.entry_directory.delete(0, tk.END)
        else:
            self.label_status.config(text="Por favor, insira um diretório.", fg="red")

    def command_rmdir(self):
        directory = self.entry_directory.get()
        if directory:
            self.label_status.config(text=f"Removendo o diretório {directory}", fg="green")
            self.client.send_message("rmdir " + directory)
            self.client.receive_message()
            self.entry_directory.delete(0, tk.END)
        else:
            self.label_status.config(text="Por favor, insira um diretório.", fg="red")





class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        # Vincula eventos de entrada e saída ao widget
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Exibe a tooltip ao lado do widget"""
        if self.tip_window:
            return

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30  # Posicionamento
        y += self.widget.winfo_rooty() + 30

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)  # Remove bordas
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tip_window, text=self.text, bg="lightyellow", 
                         relief="solid", borderwidth=1, font=("Tahoma", 10))
        label.pack()

    def hide_tooltip(self, event=None):
        """Remove a tooltip quando o mouse sai do widget"""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
