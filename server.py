import os
import json
import socket
import threading
import subprocess
from utils import verificaUser

class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        """Inicializa o servidor com host e porta padrão"""
        self.host = host  # Endereço IP do servidor
        self.port = port  # Porta do servidor
        self.server_socket = None  # Socket do servidor
        self.client_sockets = []  # Lista de sockets de clientes conectados
        self.running = False  # Estado do servidor (inicialmente parado)

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

                # Lida com o login
                if message.startswith("login"):
                    # Extrai o usuário e a senha
                    parts = message.split()
                    if len(parts) == 3:
                        username = parts[1]
                        password = parts[2]
                        if self.verificaUser(username, password, "../users/user_data.bin"):
                            response = "Login bem sucedido"
                        else:
                            response = "Usuário ou senha inválidos"
                    else:
                        response = "Requisição de login inválida"
                else:
                    response = f"Comando não reconhecido: {message}"

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
                    
                if not (message.startswith("get") or message.startswith("put")):
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

    def command_ls(self):
        """Executa o comando 'ls' para listar arquivos no diretório atual"""
        try:
            result = subprocess.run(['ls'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout if result.stdout else "Diretório vazio"
            return result.stderr
        except Exception as e:
            return f"Erro ao executar 'ls': {e}"

    def command_cd(self, message):
        """Executa o comando 'cd' para mudar de diretório"""
        file_name = message[3:].strip()  # Extrai o nome do diretório
        try:
            os.chdir(file_name)  # Muda o diretório de trabalho
            return f"Diretório alterado para: {os.getcwd()}"
        except FileNotFoundError:
            return f"Erro: Diretório '{file_name}' não encontrado."
        except Exception as e:
            return f"Erro ao executar 'cd': {e}"

    def command_mkdir(self, message):
        """Executa o comando 'mkdir' para criar diretório"""
        dir_name = message[6:].strip()  # Extrai o nome do diretório
        try:
            result = subprocess.run(['mkdir', dir_name], capture_output=True, text=True)
            return f"Diretório '{dir_name}' criado com sucesso." if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erro ao executar 'mkdir': {e}"

    def command_rmdir(self, message):
        """Executa o comando 'rmdir' para remover diretório"""
        dir_name = message[6:].strip()  # Extrai o nome do diretório
        try:
            result = subprocess.run(['rmdir', dir_name], capture_output=True, text=True)
            return f"Diretório '{dir_name}' removido com sucesso." if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erro ao executar 'rmdir': {e}"

    def command_get(self, message, client_socket):
        """Prepara para enviar arquivo ao cliente (comando 'get')"""
        file_name = message[4:].strip()
        client_socket.sendall("READY".encode())  # Envia confirmação
        return self.send_file(file_name, client_socket)  # Envia o arquivo

    def command_put(self, message, client_socket):
        """Prepara para receber arquivo do cliente (comando 'put')"""
        file_name = message[4:].strip()
        client_socket.sendall("READY".encode())  # Envia confirmação
        return self.receive_file(file_name, client_socket)  # Recebe o arquivo

    def send_file(self, file_name, target_socket):
        """Envia um arquivo para o cliente em blocos de 1024 bytes"""
        try:
            with open(file_name, "rb") as file:
                file_size = os.path.getsize(file_name)
                print(f"Enviando arquivo: {file_name} ({file_size} bytes)")
                
                # Envia o arquivo em blocos
                bytes_sent = 0
                while bytes_sent < file_size:
                    data = file.read(1024)
                    target_socket.sendall(data)
                    bytes_sent += len(data)
                
                # Envia marcador de fim de arquivo
                target_socket.sendall(b"<<EOF>>")
                print(f"Arquivo '{file_name}' enviado com sucesso")
                return None
        except FileNotFoundError:
            return f"Erro: Arquivo '{file_name}' não encontrado"
        except Exception as e:
            return f"Erro ao executar 'get': {e}"

    def receive_file(self, file_name, origin_socket):
        """Recebe um arquivo do cliente e salva na pasta received_files"""
        try:
            
            with open(file_name, "wb") as file:
                print(f"Recebendo arquivo: {file_name}")
                
                while True:
                    data = origin_socket.recv(1024)
                    if not data:
                        break  # Conexão fechada
                    
                    if b"<<EOF>>" in data:  # Verifica fim do arquivo
                        data = data.replace(b"<<EOF>>", b"")
                        file.write(data)
                        break
                    
                    file.write(data)
                
                print(f"Arquivo '{file_name}' recebido com sucesso.")
                return "Arquivo recebido com sucesso"
        except Exception as e:
            return f"Erro ao receber arquivo: {e}"