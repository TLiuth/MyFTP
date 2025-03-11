import socket
import sys
import os

import socket

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host  # Endereço IP do servidor
        self.port = port  # Porta do servidor
        self.socket = None  # Socket do cliente
        self.id_num = 0

    def connect(self):
        """Conecta ao servidor."""
        try:
            # Cria um socket TCP/IP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Conecta ao servidor
            self.socket.connect((self.host, self.port))
            print(f"Conectado ao servidor {self.host}:{self.port}")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")

    def send_message(self, message):
        """Envia uma mensagem para o servidor."""
        try:
            if self.socket:
                # Envia a mensagem codificada em bytes
                self.socket.sendall(message.encode())
                print(f"Mensagem enviada: {message}")
            else:
                print("Erro: Cliente não está conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    def receive_message(self):
        """Recebe uma mensagem do servidor."""
        try:
            if self.socket:
                # Recebe a mensagem do servidor (tamanho máximo de 1024 bytes)
                data = self.socket.recv(1024)
                if data:
                    print(f"--------------------\nMensagem recebida:\n{data.decode()}\n--------------------")
                else:
                    print("Conexão fechada pelo servidor.")
            else:
                print("Erro: Cliente não está conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

    def disconnect(self):
        """Encerra a conexão com o servidor."""
        try:
            if self.socket:
                self.socket.close()
                print("Conexão encerrada.")
            else:
                print("Erro: Cliente não está conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao encerrar conexão: {e}")

    def greet(self):
        """Mensagem de saudação."""
        print("Conectado ao servidor")

    def send_file(self, file_name, target_socket):
        """ Function to send a file back """
        try:
            with open(file_name, "rb") as file:
                print(f">> Enviando arquivo: {file_name}")
                while True:
                    data = file.read(1024) # lê 1024 bytes do arquivo
                    if not data:
                        break
                    target_socket.sendall(data)
                print(f"Arquivo '{file_name}' enviado com sucesso")
                return ">> Arquivo buscado com sucesso"
        except FileNotFoundError:
            return f"Erro: Arquivo '{file_name}' não encontrado"
        except Exception as e:
            return f"Erro ao executar 'get': {e}"

    def receive_file(self, file_name, origin_socket):
        """Função para receber um arquivo."""
        try:
            with open(file_name, "wb") as file:
                print(f"Recebendo arquivo: {file_name}")

                while True:
                    data = origin_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)

                print(f"Arquivo '{file_name}' recebido com sucesso.")
                return ">> Arquivo enviado com sucesso."
        except FileNotFoundError:
            return f"Erro: Não foi possível criar o arquivo '{file_name}'"
        except Exception as e:
            return f"Erro ao receber arquivo: {e}"