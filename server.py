import socket
import sys
import os

import socket
import threading
import subprocess

from IPython.utils.capture import capture_output
from mako.runtime import capture


class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host  # Endereço IP do servidor
        self.port = port  # Porta do servidor
        self.server_socket = None  # Socket do servidor
        self.client_sockets = []  # Lista de sockets de clientes conectados

    def start(self):
        """Inicia o servidor e escuta por conexões de clientes."""
        try:
            # Cria um socket TCP/IP
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Associa o socket ao endereço e porta
            self.server_socket.bind((self.host, self.port))
            # Escuta por conexões (até 5 clientes na fila)
            self.server_socket.listen(5)
            print(f"Servidor escutando em {self.host}:{self.port}...")

            while True:
                # Aceita uma nova conexão
                client_socket, client_address = self.server_socket.accept()
                print(f"Conexão estabelecida com {client_address}")
                self.client_sockets.append(client_socket)

                # Inicia uma nova thread para tratar a conexão do cliente
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"Erro ao iniciar o servidor: {e}")
        finally:
            self.stop()

    def handle_client(self, client_socket):
        """Lida com a comunicação de um cliente."""
        try:
            while True:
                # Recebe a mensagem do cliente
                data = client_socket.recv(1024)
                if not data:
                    break  # Se não houver dados, encerra a conexão

                # Decodifica a mensagem e exibe
                complete_message = data.decode()
                message = data.decode().strip()
                print(f"Mensagem recebida: {complete_message}")
                print(f"Test message: {message}")
                if message.startswith("ls"):
                    response = self.command_ls()
                elif message.startswith("cd"):
                    response = self.command_cd(message)
                elif message.startswith("cd.."):
                    response = self.command_cdback()
                elif message.startswith("mkdir"):
                    response = self.command_mkdir(message)
                elif message.startswith("rmdir"):
                    response = self.command_rmdir(message)
                elif message.startswith("get"):
                    break
                elif message.startswith("put"):
                    break
                else:
                    response = f"Comando não reconhecido: {message}"

                print(f"RESPONSE: {message}")


                # Envia uma resposta ao cliente
                client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Erro ao lidar com o cliente: {e}")
        finally:
            # Fecha a conexão com o cliente
            client_socket.close()
            self.client_sockets.remove(client_socket)
            print("Conexão com o cliente encerrada.")

    def stop(self):
        """Encerra o servidor e fecha todas as conexões."""
        try:
            # Fecha todos os sockets de clientes
            for client_socket in self.client_sockets:
                client_socket.close()
            # Fecha o socket do servidor
            if self.server_socket:
                self.server_socket.close()
            print("Servidor encerrado.")
        except Exception as e:
            print(f"Erro ao encerrar o servidor: {e}")

    def greet(self):
        """Mensagem de saudação."""
        print("Conectado ao cliente")

    def command_ls(self):
        """ Executa o comando 'ls'"""
        print(">> Executando ls")
        try:
            result = subprocess.run(['ls'], capture_output=True, text=True)
            if result.returncode == 0:
                if not result.stdout:
                    return "Diretório vazio"

                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            return f"Erro ao executar 'ls': {e}"

    def command_cd(self, message):
        """ Executando o comando 'cd'"""
        print(">> Executando cd")
        file_name = message[3:].strip()

        try:
            # Usa os.chdir para mudar o diretório de trabalho do processo atual
            os.chdir(file_name)
            # Retorna o novo diretório de trabalho
            return f"Diretório alterado para: {os.getcwd()}"
        except FileNotFoundError:
            return f"Erro: Diretório '{file_name}' não encontrado."
        except Exception as e:
            return f"Erro ao executar 'cd': {e}"

    def command_cdback(self):
        """ Executando o comando 'cd..'"""
        print(">> Executando cd ..")
        file_name = ".."
        print(f"Tentando mudar para o diretório: {file_name}")

        try:
            # Usa os.chdir para mudar o diretório de trabalho do processo atual
            os.chdir(file_name)
            # Retorna o novo diretório de trabalho
            return f"Diretório alterado para: {os.getcwd()}"
        except FileNotFoundError:
            return f"Erro: Diretório '{file_name}' não encontrado."
        except Exception as e:
            return f"Erro ao executar 'cdback': {e}"

    def command_mkdir(self, message):
        """ Executando o comando 'mkdir'"""
        print(">> Executando mkdir")

        file_name = message[6:].strip()

        try:
            result = subprocess.run(['mkdir', file_name], capture_output=True, text=True)
            return f"Diretório '{file_name}' criado com sucesso." if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erro ao executar 'mkdir': {e}"

    def command_rmdir(self, message):
        """ Executando o comando 'rmdir'"""
        print(">> Executando mkdir")

        file_name = message[6:].strip()

        try:
            result = subprocess.run(['rmdir', file_name], capture_output=True, text=True)
            return f"Diretório '{file_name}' removido com sucesso." if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erro ao executar 'rmdir': {e}"