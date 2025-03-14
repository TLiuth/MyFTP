import socket
import sys
import os

import socket
import threading
import subprocess

# from IPython.utils.capture import capture_output
# from mako.runtime import capture
from werkzeug.utils import send_file


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

            # Configura a opção SO_REUSEADDR para reutilizar o socket
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Associa o socket ao endereço e porta
            self.server_socket.bind((self.host, self.port))
            self.running = True
            # Escuta por conexões (até 5 clientes na fila)
            self.server_socket.listen(5)
            print(f"Servidor escutando em {self.host}:{self.port}...")

            while self.running:
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
            while self.running:
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
                    response = self.command_get(message, client_socket)
                elif message.startswith("put"):
                    response = self.command_put(message, client_socket)
                else:
                    response = f"Comando não reconhecido: {message}"

                # Envia uma resposta ao cliente
                client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Erro ao lidar com o cliente: {e}")
        finally:
            # Fecha a conexão com o cliente
            client_socket.close()
            if client_socket in self.client_sockets:
                self.client_sockets.remove(client_socket)

    def stop(self):
        """Encerra o servidor e fecha todas as conexões."""
        try:
            # Sinaliza para parar o loop de aceitação de conexões
            self.running = False

            # Fecha todos os sockets de clientes
            for client_socket in self.client_sockets:
                client_socket.close()
            self.client_sockets.clear()

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

    def command_get(self, message, client_socket):
        """ Executando o comando 'get'"""
        print(">> Executando get")

        file_name = message[4:].strip()
        
        client_socket.sendall("READY".encode())

        return self.send_file(file_name, client_socket)

    def command_put(self, message, client_socket):
        """ Executando o comando 'put'"""
        print(">> Executando put")

        file_name = message[4:].strip()
        
        client_socket.sendall("READY".encode())

        return self.receive_file(file_name, client_socket)

    def send_file(self, file_name, target_socket):
        """Envia um arquivo para o cliente."""
        try:
            with open(file_name, "rb") as file:
                print(f">> Enviando arquivo: {file_name}")
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    target_socket.sendall(data)
                target_socket.sendall(b"<<EOF>>")  # Envia um marcador para indicar fim da transmissão
                print(f"Arquivo '{file_name}' enviado com sucesso")
                return ">> Arquivo buscado com sucesso"
        except FileNotFoundError:
            return f"Erro: Arquivo '{file_name}' não encontrado"
        except Exception as e:
            return f"Erro ao executar 'get': {e}"



    def receive_file(self, file_name, origin_socket):
        """Função para receber um arquivo."""
        try:
            # Define o caminho da pasta 'received_files'
            received_folder = "received_files"

            # Cria a pasta 'received_files' se ela não existir
            if not os.path.exists(received_folder):
                os.makedirs(received_folder)
                print(f"Pasta '{received_folder}' criada.")

            # Define o caminho completo do arquivo
            file_path = os.path.join(received_folder, file_name)
            with open(file_path, "wb") as file:
                print(f">> Recebendo arquivo: {file_name}")

                while True:
                    data = origin_socket.recv(1024)
                    if not data:
                        print(">> Conexão fechada pelo servidor")
                        break

                    if b"<<EOF>>" in data:  # Se encontrar o EOF, para
                        print(">> EOF detectado. Finalizando recepção.")
                        data = data.replace(b"<<EOF>>", b"")  # Remove o EOF antes de salvar
                        file.write(data)
                        break
                    
                    print(data)
                    
                    file.write(data)
                    
                print(f"Arquivo '{file_name}' recebido com sucesso.")
                return ">> Arquivo enviado com sucesso no destino."
        except FileNotFoundError:
            return f"Erro: Não foi possível criar o arquivo '{file_name}'"
        except Exception as e:
            return f"Erro ao receber arquivo: {e}"




