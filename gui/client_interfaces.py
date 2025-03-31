import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import utils


class ClientMenu(tk.Frame):
    def __init__(self, parent, client):
        super().__init__(parent, bg="#f0f0f0")  # Inicializa o frame com cor de fundo
        self.client = client  # Armazena o cliente para comunicação
        self.load_images()  # Carrega as imagens usadas na interface
        self.create_widgets()  # Cria os componentes da interface

    def load_images(self):
        """Carrega e redimensiona imagens para os botões"""
        # Carrega cada imagem e redimensiona para o tamanho especificado
        self.img_right = self.resize_image("../images/seta_direita.png", 50, 40)
        self.img_left = self.resize_image("../images/seta_esquerda.png", 50, 40)
        self.img_cd = self.resize_image("../images/cd_icon.png", 35, 35)
        self.img_cd_up = self.resize_image("../images/cd_up_icon.png", 35, 35)
        self.img_mkdir = self.resize_image("../images/mkdir_icon.png", 35, 35)
        self.img_rmdir = self.resize_image("../images/rmdir_icon.png", 35, 35)
        self.img_ls = self.resize_image("../images/ls_icon.png", 35, 35)

        self.img_client = self.resize_image("../images/cliente_icon.png", 40, 40)
        self.img_server = self.resize_image("../images/servidor_icon.png", 30, 30)

    def resize_image(self, path, width, height):
        """Redimensiona imagem e retorna um PhotoImage"""
        image = Image.open(path)  # Abre a imagem
        image = image.resize((width, height), Image.Resampling.LANCZOS)  # Redimensiona
        return ImageTk.PhotoImage(image)  # Converte para formato Tkinter

    def create_widgets(self):
        """Cria todos os componentes da interface gráfica"""
        # Cria rótulos com ícones para cliente e servidor
        self.label_client_icon = tk.Label(self, image=self.img_client, bg="#f0f0f0")
        self.label_client_icon.place(x=60, y=5)
        self.label_client = tk.Label(self, text="Cliente", font=("Tahoma", 20, "bold"), fg="#333", bg="#f0f0f0")
        self.label_client.place(x=100, y=15, anchor="nw")

        self.label_server_icon = tk.Label(self, image=self.img_server, bg="#f0f0f0")
        self.label_server_icon.place(x=565, y=15, anchor="ne")
        self.label_server = tk.Label(self, text="Servidor", font=("Tahoma", 20, "bold"), fg="#333", bg="#f0f0f0")
        self.label_server.place(x=700, y=15, anchor="ne")

        # Listboxes para mostrar arquivos do cliente e servidor
        self.listbox_client = tk.Listbox(self, height=15, width=30, bg="white", fg="#222", font=("Tahoma", 12))
        self.listbox_client.place(x=20, y=70, anchor="nw")
        self.command_ls_client()  # Lista arquivos do cliente inicialmente
        
        self.listbox_server = tk.Listbox(self, height=15, width=30, bg="white", fg="#222", font=("Tahoma", 12))
        self.listbox_server.place(x=780, y=70, anchor="ne")

        # Rótulo e campo de entrada para comandos de diretório
        self.entry_label = tk.Label(self, text="Diretório:", font=("Tahoma", 10, "bold"), fg="#333", bg="#f0f0f0")
        self.entry_label.place(x=225, y=460, anchor="nw")

        self.entry_directory = tk.Entry(self, width=20, font=("Tahoma", 12))
        self.entry_directory.place(x=300, y=460, anchor="nw")

        # Configuração de estilo para os botões
        button_style = {"bd": 2, "bg": "white", "fg": "white", "activebackground": "#45a049",
                        "font": ("Tahoma", 12, "bold")}

        # Criação dos botões com ícones e tooltips
        self.button_ls = tk.Button(self, image=self.img_ls, command=self.command_ls, **button_style)
        self.button_ls.place(x=280, y=400)
        ToolTip(self.button_ls, "Listar arquivos")

        self.button_cd = tk.Button(self, image=self.img_cd, command=self.command_cd, **button_style)
        self.button_cd.place(x=330, y=400)
        ToolTip(self.button_cd, "Mudar de diretório")

        self.button_cd_up = tk.Button(self, image=self.img_cd_up, command=self.command_cd_up, **button_style)
        self.button_cd_up.place(x=380, y=400)
        ToolTip(self.button_cd_up, "Voltar um diretório")

        self.button_mkdir = tk.Button(self, image=self.img_mkdir, command=self.command_mkdir, **button_style)
        self.button_mkdir.place(x=430, y=400)
        ToolTip(self.button_mkdir, "Criar diretório")

        self.button_rmdir = tk.Button(self, image=self.img_rmdir, command=self.command_rmdir, **button_style)
        self.button_rmdir.place(x=480, y=400)
        ToolTip(self.button_rmdir, "Remover diretório")

        # Rótulo para mensagens de status
        self.label_status = tk.Label(self, text="", fg="red", font=("Consolas", 10, "bold"), bg="#f0f0f0")
        self.label_status.place(x=525, y=415)

        # Botões centrais para transferência de arquivos
        self.button_right = tk.Button(self, image=self.img_right, command=self.move_to_server, **button_style)
        self.button_right.place(relx=0.5, rely=0.4, anchor="center")
        ToolTip(self.button_right, "Enviar arquivo")

        self.button_left = tk.Button(self, image=self.img_left, command=self.move_to_client, **button_style)
        self.button_left.place(relx=0.5, rely=0.6, anchor="center")
        ToolTip(self.button_left, "Requisitar arquivo")

    def move_to_server(self):
        """Envia arquivo selecionado do cliente para o servidor"""
        selected = self.listbox_client.curselection()
        if selected:
            item = self.listbox_client.get(selected)
            self.listbox_server.insert("end", item)  # Adiciona visualmente ao servidor
            self.client.send_message("put " + item)  # Envia comando para o servidor

    def move_to_client(self):
        """Solicita arquivo do servidor para o cliente"""
        selected = self.listbox_server.curselection()
        if selected:
            item = self.listbox_server.get(selected)
            self.listbox_client.insert("end", item)  # Adiciona visualmente ao cliente
            self.client.send_message("get " + item)  # Envia comando para o servidor

    def command_ls(self):
        """Lista arquivos no servidor"""
        self.label_status.config(text="Listando arquivos", fg="green")
        self.client.send_message("ls")  # Envia comando ls
        files = self.client.receive_message().strip()  # Recebe lista de arquivos

        if files:  # Se houver arquivos
            file_list = files.split("\n")  # Divide por linhas
            self.listbox_server.delete(0, tk.END)  # Limpa listbox
            for file in file_list:
                if file.strip():  # Ignora linhas vazias
                    self.listbox_server.insert(tk.END, file)  # Adiciona cada arquivo
        self.command_ls_client()  # Atualiza lista do cliente também
                    
    def command_ls_client(self):
        """Lista arquivos no diretório local do cliente"""
        try:
            # Executa comando ls localmente
            result = subprocess.run(['ls'], capture_output=True, text=True)
            if result.returncode == 0:
                if not result.stdout:
                    return None
                files = result.stdout.strip()  # Obtém saída do comando
                file_list = files.split("\n")  # Divide por linhas
                self.listbox_client.delete(0, tk.END)  # Limpa listbox
                for file in file_list:
                    if file.strip():  # Ignora linhas vazias
                        self.listbox_client.insert(tk.END, file)  # Adiciona cada arquivo
            else:
                return result.stderr  # Retorna erro se houver
        except Exception as e:
            return f"Erro ao executar 'ls': {e}"  # Retorna mensagem de erro

    def command_cd(self):
        """Muda diretório no servidor"""
        selected = self.listbox_server.curselection()
        if selected:
            directory = self.listbox_server.get(selected)  # Pega diretório selecionado
            self.label_status.config(text=f"Mudando para {directory}", fg="green")
            self.client.send_message("cd " + directory)  # Envia comando cd
            self.client.receive_message()  # Aguarda resposta
            self.command_ls()  # Atualiza lista de arquivos
        else:
            self.label_status.config(text="Por favor, insira um diretório.", fg="red")

    def command_cd_up(self):
        """Volta um diretório no servidor"""
        self.label_status.config(text="Voltando um diretório", fg="green")
        self.client.send_message("cd ..")  # Envia comando para voltar
        self.client.receive_message()  # Aguarda resposta
        self.entry_directory.delete(0, tk.END)  # Limpa campo de entrada
        self.command_ls()  # Atualiza lista de arquivos

    def command_mkdir(self):
        """Cria novo diretório no servidor"""
        directory = self.entry_directory.get()  # Pega nome do campo de entrada
        if directory:
            self.label_status.config(text=f"Criando o diretório {directory}", fg="green")
            self.client.send_message("mkdir " + directory)  # Envia comando mkdir
            self.client.receive_message()  # Aguarda resposta
            self.entry_directory.delete(0, tk.END)  # Limpa campo
            self.command_ls()  # Atualiza lista
        else:
            self.label_status.config(text="Por favor, insira um diretório.", fg="red")

    def command_rmdir(self):
        """Remove diretório no servidor"""
        selected = self.listbox_server.curselection()
        if selected:
            directory = self.listbox_server.get(selected)  # Pega diretório selecionado
            self.label_status.config(text=f"Removendo o diretório {directory}", fg="green")
            self.client.send_message("rmdir " + directory)  # Envia comando rmdir
            self.client.receive_message()  # Aguarda resposta
            self.command_ls()  # Atualiza lista
        else:
            self.label_status.config(text="Por favor, insira um diretório.", fg="red")


class LoginMenu(ttk.Frame):
    def __init__(self, parent, on_login_success):
        """Frame de login com campos para usuário e senha"""
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success  # Callback para login bem-sucedido
        self.create_widgets()  # Cria componentes

    def create_widgets(self):
        """Cria interface de login"""
        self.pack(expand=True, fill="both")  # Expande para ocupar todo espaço

        # Frame central para os componentes de login
        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza

        # Rótulos e campos de entrada
        self.label_username = tk.Label(frame, text="Username: ")
        self.label_username.pack(pady=5)

        self.entry_username = tk.Entry(frame)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(frame, text="Senha:")
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(frame, show="*")  # Oculta senha
        self.entry_password.pack(pady=5)

        # Botão de login
        self.button_login = tk.Button(frame, text="Login", command=self.on_click_login)
        self.button_login.pack(pady=10)

        # Rótulo para mensagens de status
        self.label_status = tk.Label(frame, text="", fg="red")
        self.label_status.pack(pady=5)

    def on_click_login(self):
        """Valida credenciais ao clicar no botão de login"""
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Verifica credenciais no arquivo de usuários
        if utils.verificaUser(username, password, "../users/user_data.bin"):
            messagebox.showinfo("Login", "Login bem sucedido!")
            self.on_login_success()  # Chama callback de sucesso
            self.pack_forget()  # Esconde o menu de login
        else:
            self.label_status.config(text="Usuário ou senha incorretos.", fg="red")


class ToolTip:
    """Classe para criar tooltips (dicas) para widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None  # Janela da tooltip

        # Vincula eventos do mouse
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Exibe a tooltip quando o mouse entra no widget"""
        if self.tip_window:
            return

        # Calcula posição para exibir a tooltip
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 30

        # Cria janela temporária para a tooltip
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)  # Remove bordas da janela
        self.tip_window.wm_geometry(f"+{x}+{y}")  # Posiciona

        # Cria rótulo com o texto da tooltip
        label = tk.Label(self.tip_window, text=self.text, bg="lightyellow",
                         relief="solid", borderwidth=1, font=("Tahoma", 10))
        label.pack()

    def hide_tooltip(self, event=None):
        """Remove a tooltip quando o mouse sai do widget"""
        if self.tip_window:
            self.tip_window.destroy()  # Destroi a janela
            self.tip_window = None