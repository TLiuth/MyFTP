from client import Client
from server import Server
from utils import verificaUser


def DEBUGMODE():
    return True

def login_request():
    while True and not DEBUGMODE():
        user = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")
        if verificaUser(user, senha, "../users/user_data.bin"):
            break

def main():

    login_request()


    print("1 - INICIAR CLIENTE\n2 - INICIAR SERVIDOR\n")
    opcao = str(input("Digite a opção desejada: "))

    while opcao != "0":
        if opcao == "1":
            main_client()

            break
        elif opcao == "2":
            ip = str(input("Digite um IP, ou 0 pro IP local: "))
            if ip == '0':
                ip = '127.0.0.1'
            server = Server(host=f'{ip}', port=12345)
            try:
                # Inicia o servidor
                server.start()
            except KeyboardInterrupt:
                # Encerra o servidor ao pressionar Ctrl+C
                server.stop()
            break
        else:
            print("Opção inválida")

        opcao = input("Digite a opção desejada: ")

# trata do fluxo principal do cliente
def main_client():
    ip = str(input("Digite um IP, ou 0 pro IP local: "))
    if ip == '0':
        ip = '127.0.0.1'
    client = Client(host=f'{ip}', port=12345)
    client.connect()
    
    # server_listener = threading.Thread(target=client.handle_server, daemon=True)
    # server_listener.start()
    
    
    print("Digite FIM para encerrar a conexão")
    mensagem = str(input("Digite uma mensagem: "))
    while mensagem != "FIM":

        # encerra o loop e desconecta
        if mensagem == "FIM":
            break

        # demais comandos serão processados no server por meio do envio de mensagem
        # Envia uma mensagem
        client.send_message(mensagem)

        if not (mensagem.startswith("get") or mensagem.startswith("put")):
            # Recebe uma resposta
            client.receive_message()

        mensagem = str(input("Digite uma mensagem: "))

    # Encerra a conexão
    client.disconnect()

# trata do fluxo principal do server
def main_server():
    pass

if __name__ == "__main__":
    main()