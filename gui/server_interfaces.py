# Importações necessárias para a interface gráfica e funcionalidades
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

# Adiciona o diretório pai ao path para importar módulos
sys.path.append('../')
from server import Server
from client import Client
import threading
import client_interfaces

# Classe principal que representa o menu de serviços
class ServiceMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()  # Cria os widgets da interface
        self.ip = ""  # Variável para armazenar o IP

    # Método para criar os elementos da interface
    def create_widgets(self):
        # Expande o frame para preencher todo o espaço disponível
        self.pack(expand=True, fill="both")

        # Cria um frame interno para centralizar os widgets
        self.frame = tk.Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona no centro

        # Botão para iniciar o cliente
        self.button_startClient = tk.Button(self.frame, text="Start Client", command=self.on_click_client_verify_login,
                                            width=10, height=2)
        self.button_startClient.pack(pady=10)  # Adiciona espaçamento
        self.button_startClient.config(state=tk.ACTIVE)  # Define como ativo inicialmente

        # Botão para iniciar o servidor
        self.button_startServer = tk.Button(self.frame, text="Start Server", command=self.on_click_server, width=10,
                                            height=2)
        self.button_startServer.pack(pady=10)  # Adiciona espaçamento
        self.button_startServer.config(background="orange")  # Cor de fundo laranja

        # Campo de entrada para o IP
        self.entry_ip = tk.Entry(self.frame, background="orange")
        self.entry_ip.insert(0, '127.0.0.1')  # Valor padrão (localhost)
        self.entry_ip.pack(pady=5)  # Adiciona espaçamento

    # Método chamado quando o botão de iniciar servidor é clicado
    def on_click_server(self):
        try:
            # Obtém o IP do campo de entrada
            ip = self.entry_ip.get()
            # Cria uma instância do servidor
            self.server = Server(host=f'{ip}', port=12345)
            # Inicia o servidor em uma thread separada (para não bloquear a interface)
            server_thread = threading.Thread(target=self.server.start, daemon=True)
            server_thread.start()

            # Mostra um label indicando que o servidor está rodando
            self.label_iniciado = tk.Label(self.frame, text=f"Server running on {ip}!")
            self.label_iniciado.pack(pady=10)
            # Botão para parar o servidor
            self.button_stopServer = tk.Button(self.frame, text="Stop Server", background="red",
                                               command=self.on_click_stop_server)
            self.button_stopServer.pack(pady=10)

            # Desabilita os botões de iniciar servidor e cliente
            self.button_startServer.config(state=tk.DISABLED)
            self.button_startClient.config(state=tk.DISABLED)
        except Exception as e:
            # Mostra mensagem de erro se algo falhar
            messagebox.showerror("Server Error", f"Failed to start server: {e}")

    # Método chamado quando o cliente é iniciado (após login)
    def on_click_client(self):
        ip = self.ip
        # Cria uma instância do cliente e conecta ao servidor
        client = Client(host=f"{ip}", port=12345)
        client.connect()
        self.pack_forget()  # Esconde o menu de serviços
        # Mostra o menu do cliente
        self.client_menu = client_interfaces.ClientMenu(self.master, client)
        self.client_menu.pack(expand=True, fill="both")

    # Método chamado quando o botão de iniciar cliente é clicado
    def on_click_client_verify_login(self):
        # Armazena o IP para uso posterior
        self.ip = self.entry_ip.get()
        self.pack_forget()  # Esconde o menu de serviços

        # Mostra o menu de login, passando uma callback para quando o login for bem-sucedido
        self.login_menu = client_interfaces.LoginMenu(self.master, on_login_success=self.on_click_client)
        self.login_menu.pack(expand=True, fill="both")

    # Método chamado quando o botão de parar servidor é clicado
    def on_click_stop_server(self):
        self.server.stop()  # Para o servidor
        # Remove os elementos da interface relacionados ao servidor rodando
        self.label_iniciado.pack_forget()
        self.button_stopServer.pack_forget()

        # Reabilita os botões de iniciar servidor e cliente
        self.button_startServer.config(state=tk.NORMAL)
        self.button_startClient.config(state=tk.NORMAL)

        # Mostra mensagem informando que o servidor foi encerrado
        messagebox.showinfo("Server", "Servidor encerrado!")
        exit(1)  # Encerra o programa