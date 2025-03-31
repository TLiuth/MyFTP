import json
import socket

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        # Inicializa o cliente com endereço e porta do servidor
        self.host = host  # Endereço IP do servidor (padrão: localhost)
        self.port = port  # Porta do servidor (padrão: 12345)
        self.socket = None  # Socket de conexão (inicialmente None)
        self.id_num = 0  # ID numérico do cliente (não utilizado atualmente)

    def connect(self):
        """Estabelece conexão com o servidor."""
        try:
            # Cria um socket TCP/IP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Conecta ao servidor usando host e porta especificados
            self.socket.connect((self.host, self.port))
            print(f"Conectado ao servidor {self.host}:{self.port}")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            
    def send_message(self, message):
        """
        Envia mensagem para o servidor, com tratamento especial para comandos put/get.
        """
        try:
            if not self.socket:
                print("Erro: Cliente não está conectado ao servidor.")
                return

            # Divide o comando em partes (comando + argumento)
            command_parts = message.split(maxsplit=1)
            command = command_parts[0].lower()

            # Tratamento especial para comandos put e get
            if command in ("put", "get"):
                if len(command_parts) < 2:
                    print(f"Erro: Comando '{command}' requer um nome de arquivo.")
                    return

                file_name = command_parts[1].strip()
                self.socket.sendall(message.encode())  # Envia o comando
                response = self.socket.recv(1024).decode()  # Aguarda confirmação

                if response == "READY":
                    if command == "put":
                        self.send_file(file_name, self.socket)  # Envia arquivo para servidor
                    elif command == "get":
                        self.receive_file(file_name, self.socket)  # Recebe arquivo do servidor
                else:
                    print(f"Erro: {response}")  # Mostra mensagem de erro do servidor
            else:
                # Comandos normais (não put/get) são enviados diretamente
                self.socket.sendall(message.encode())
                print(f"Mensagem enviada: {message}")

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    def receive_message(self):
        """Recebe e exibe mensagens do servidor."""
        try:
            if self.socket:
                # Recebe dados do servidor (buffer de 1024 bytes)
                data = self.socket.recv(1024)
                if data:
                    # Exibe mensagem formatada
                    print(f"--------------------\nMensagem recebida:\n{data.decode()}\n--------------------")
                    return data.decode()
                else:
                    print("Conexão fechada pelo servidor.")
            else:
                print("Erro: Cliente não está conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

    def disconnect(self):
        """Fecha a conexão com o servidor."""
        try:
            if self.socket:
                self.socket.close()
                print("Conexão encerrada.")
            else:
                print("Erro: Cliente não está conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao encerrar conexão: {e}")

    def greet(self):
        """Método de saudação (não utilizado atualmente)."""
        print("Conectado ao servidor")

    def send_file(self, file_name, target_socket):
        """
        Envia arquivo para o servidor/cliente conectado.
        """
        try:
            with open(file_name, "rb") as file:
                print(f">> Enviando arquivo: {file_name}")
                while True:
                    data = file.read(1024)  # Lê em chunks de 1KB
                    if not data:
                        break
                    target_socket.sendall(data)  # Envia dados
                # Envia marcador de fim de arquivo
                target_socket.sendall(b"<<EOF>>")
                print(f"Arquivo '{file_name}' enviado com sucesso")
        except FileNotFoundError:
            return f"Erro: Arquivo '{file_name}' não encontrado"
        except Exception as e:
            return f"Erro ao executar 'get': {e}"

    def receive_file(self, file_name, origin_socket):
        """
        Recebe arquivo do servidor/cliente.
        """
        try:
            with open(f'{file_name}', "wb") as file:
                print(f"Recebendo arquivo: {file_name}")

                while True:
                    data = origin_socket.recv(1024)  # Recebe dados em chunks
                    if not data:
                        print(">> Conexão fechada pelo servidor")
                        break

                    # Verifica marcador de fim de arquivo
                    if b"<<EOF>>" in data:
                        print(">> EOF detectado. Finalizando recepção.")
                        data = data.replace(b"<<EOF>>", b"")
                        file.write(data)
                        break
                    
                    file.write(data)

                print(f"Arquivo '{file_name}' recebido com sucesso.")
                return ">> Arquivo recebido com sucesso."
        except Exception as e:
            return f"Erro ao receber arquivo: {e}"