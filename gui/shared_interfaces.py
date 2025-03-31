import tkinter as tk
import sys
sys.path.append('../')  # Adiciona o diretório pai ao path para importar módulos

# Importa a interface do servidor
import server_interfaces

class App(tk.Tk):
    def __init__(self, title, size):
        """Classe principal da aplicação que herda de tk.Tk (janela principal)"""
        
        # Configuração inicial da janela principal
        super().__init__()  # Inicializa a classe pai (tk.Tk)
        self.title(title)  # Define o título da janela
        self.geometry(f"{size[0]}x{size[1]}")  # Define tamanho inicial (largura x altura)
        self.minsize(size[0], size[1])  # Define tamanho mínimo da janela

        # Cria e exibe o menu de serviço inicial
        self.service_menu = server_interfaces.ServiceMenu(self)  # Instancia o menu de serviço
        self.service_menu.pack(expand=True, fill="both")  # Empacota para preencher toda a janela

        # Inicia o loop principal da aplicação
        self.mainloop()  # Mantém a janela aberta e responde a eventos

# Cria e executa a aplicação com título "MyFTP" e tamanho 800x500 pixels
App("MyFTP", (800, 500))