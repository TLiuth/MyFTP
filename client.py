import json

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
        """Envia uma mensagem para o servidor, tratando comandos put e get corretamente."""
        try:
            if not self.socket:
                print("Erro: Cliente não está conectado ao servidor.")
                return

            command_parts = message.split(maxsplit=1)
            command = command_parts[0].lower()

            if command in ("put", "get"):
                if len(command_parts) < 2:
                    print(f"Erro: Comando '{command}' requer um nome de arquivo.")
                    return

                file_name = command_parts[1].strip()
                self.socket.sendall(message.encode())  # Envia o comando
                response = self.socket.recv(1024).decode()  # Aguarda resposta do servidor
                print(response)

                if response == "READY":
                    if command == "put":
                        self.send_file(file_name, self.socket)
                    elif command == "get":
                        self.receive_file(file_name, self.socket)
                    # final_response = self.socket.recv(1024).decode()
                    # print(f"Resposta final do servidor: {final_response}")
                else:
                    print(f"Erro: {response}")

            else:
                self.socket.sendall(message.encode())  # Envia comandos normais
                print(f"Mensagem enviada: {message}")

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
                    return data.decode()
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

    def send_login(self, username, password, path):
        """Sends a login request to the server."""
        login_data = {"command": "login", "username": username, "password": password, "path": path}
        self.socket.sendall(json.dumps(login_data).encode())
        response = self.socket.recv(1024).decode()
        return response

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
                return # ">> Arquivo buscado com sucesso"
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
                    print(f"Recebido {len(data)} bytes: {data}")  # Log para depuração                    
                    if not data:
                        print(">> Conexão fechada pelo servidor")
                        break

                    if b"<<EOF>>" in data:  # Se encontrar o EOF, para
                        print(">> EOF detectado. Finalizando recepção.")
                        data = data.replace(b"<<EOF>>", b"")  # Remove o EOF antes de salvar
                        file.write(data)
                        break
                                        
                    file.write(data)

                print(f"Arquivo '{file_name}' recebido com sucesso.")
                return ">> Arquivo recebido com sucesso."
        except Exception as e:
            return f"Erro ao receber arquivo: {e}"
